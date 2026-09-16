import importlib.util
import json
from pathlib import Path
import tempfile
import unittest
import threading
from urllib.request import urlopen, Request
from urllib.error import HTTPError

import alina
import study
from unittest.mock import patch
from extract import extract


class AlinaTests(unittest.TestCase):
    def test_pdf_batches_resume_and_finish_without_duplicate_chunks(self):
        from reportlab.pdfgen.canvas import Canvas
        p=self.sources/'large.pdf'
        canvas=Canvas(str(p))
        for page in range(17):
            canvas.drawString(50,750,f'Page {page+1}: persistent extraction test')
            canvas.showPage()
        canvas.save()
        alina.scan();alina.process_one()
        self.assertEqual(alina.snapshot()['counts']['pending'],1)
        with alina.connection() as db:
            self.assertEqual(db.execute('SELECT next FROM pdf_progress').fetchone()[0],8)
            self.assertEqual(db.execute('SELECT count(*) FROM chunks').fetchone()[0],8)
        alina.init();alina.process_one();alina.process_one()
        self.assertEqual(alina.snapshot()['counts']['ready'],1)
        self.assertEqual(alina.snapshot()['chunks'],17)
        self.assertEqual(alina.snapshot()['processed'],1)
        alina.scan();self.assertFalse(alina.process_one())

    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.base=Path(self.temp.name)
        self.original_data=alina.DATA
        self.original_config=dict(alina.CONFIG)
        alina.DATA=self.base/'state'
        self.sources=self.base/'sources';self.sources.mkdir()
        alina.CONFIG['roots']=[str(self.sources)]
        alina.init()
    def tearDown(self):
        alina.DATA=self.original_data
        alina.CONFIG.clear();alina.CONFIG.update(self.original_config)
        self.temp.cleanup()
    def test_incremental_scan_extract_dedup(self):
        p=self.sources/'source.md';p.write_text('Проверяемая информация\nДля поиска',encoding='utf-8')
        alina.scan();self.assertEqual(alina.snapshot()['counts']['pending'],1)
        self.assertTrue(alina.process_one())
        before=alina.snapshot();self.assertEqual(before['counts']['ready'],1)
        alina.scan();self.assertFalse(alina.process_one())
        (self.sources/'duplicate.md').write_bytes(p.read_bytes())
        alina.scan();alina.process_one()
        self.assertEqual(alina.snapshot()['chunks'],before['chunks'])
        p.write_text('Другая версия',encoding='utf-8')
        alina.scan();alina.process_one()
        self.assertEqual(alina.snapshot()['processed'],3)
    def test_failure_is_not_processed(self):
        (self.sources/'broken.txt').write_bytes(b'\xff\xfe\xfd')
        alina.scan();alina.process_one()
        s=alina.snapshot();self.assertEqual(s['counts']['error'],1);self.assertEqual(s['processed'],0)
    def test_report_deltas_persist_and_reset(self):
        (self.sources/'a.txt').write_text('Test source',encoding='utf-8')
        alina.scan();alina.process_one()
        r=alina.make_report(notify=False);self.assertEqual(r['delta']['processed'],1)
        alina.init()
        r=alina.make_report(notify=False);self.assertEqual(r['delta']['processed'],0)
        self.assertEqual(len(alina.snapshot()['reports']),2)
    def test_no_source_does_not_invent_progress(self):
        alina.CONFIG['roots']=[str(self.base/'missing')]
        alina.scan();s=alina.snapshot()
        self.assertTrue(s['live']['scan_error']);self.assertEqual(s['progress'],0)
    def test_pause_persists(self):
        alina.setting('paused','true');alina.init();self.assertTrue(alina.snapshot()['paused'])
    def test_text_locator_and_hash(self):
        p=self.sources/'a.md';p.write_text('строка 1\nстрока 2',encoding='utf-8')
        result=extract(p)
        self.assertEqual(len(result['sha256']),64)
        self.assertIn('строки 1–2',result['chunks'][0]['locator'])
    def make_book(self,folder,name='book.md',text='Содержание книги. Проверяемый метод.'):
        path=self.sources/'FATHER_GOLDEN_LIBRARY'/folder/name
        path.parent.mkdir(parents=True,exist_ok=True);path.write_text(text,encoding='utf-8')
        return path
    def test_books_first_and_security_design_architecture_order(self):
        self.make_book('04_SOFTWARE_ARCHITECTURE')
        self.make_book('01_REQUIREMENTS_ANALYSIS')
        security=self.make_book('12_SECURITY')
        (self.sources/'tiny.md').write_text('x',encoding='utf-8')
        alina.scan()
        for expected in ['security','design','architecture']:
            with alina.connection() as db: row=study.next_file(db)
            self.assertEqual(study.classify(row['path'])[0],expected)
            alina.process_one()
        with alina.connection() as db:
            results=study.book_results(db,'security')
        self.assertEqual(results['books'][0]['path'],str(security))
        self.assertTrue(results['books'][0]['notes'])
        self.assertEqual(results['books'][0]['notes'][0]['excerpt'],'Содержание книги. Проверяемый метод.')
    def test_unsupported_and_duplicates_are_honest(self):
        a=self.make_book('12_SECURITY','a.md')
        self.make_book('12_SECURITY','b.md')
        self.make_book('12_SECURITY','scan.djvu')
        alina.scan();alina.process_one();alina.process_one()
        s=alina.snapshot()['study']['tracks'][0]
        self.assertEqual(s['books'],3);self.assertEqual(s['ready'],2)
        self.assertEqual(s['attention'],1);self.assertEqual(s['notes'],1)
    def test_repeat_cycle_does_not_reread_unchanged_books(self):
        self.make_book('12_SECURITY')
        alina.scan();alina.process_one();self.assertFalse(alina.process_one())
        alina.scan();self.assertFalse(alina.process_one())
        self.assertEqual(alina.snapshot()['study']['cycle'],1)
        self.make_book('04_SOFTWARE_ARCHITECTURE')
        alina.scan();self.assertEqual(alina.snapshot()['study']['cycle'],2)
    def test_manual_focus_and_stale_version_notes(self):
        old=self.make_book('12_SECURITY')
        self.make_book('04_SOFTWARE_ARCHITECTURE')
        alina.scan();alina.setting('focus_domain','architecture')
        with alina.connection() as db:self.assertEqual(study.classify(study.next_file(db)['path'])[0],'architecture')
        alina.setting('focus_domain','auto');alina.process_one()
        old.write_text('Обновлённая книга',encoding='utf-8');alina.scan()
        with alina.connection() as db:self.assertFalse(study.book_results(db,'security')['books'][0]['notes'])
    def test_file_links_are_discovered_not_silently_skipped(self):
        self.make_book('12_SECURITY')
        # Simulate a file alias without requiring Windows symlink creation privileges.
        with patch.object(Path,'is_symlink',lambda p: p.suffix=='.md'):
            alina.scan()
        self.assertEqual(alina.snapshot()['counts']['pending'],1)
    def test_search_and_local_mutation_guard(self):
        p=self.sources/'a.md';p.write_text('Проверяемая информация',encoding='utf-8')
        alina.scan();alina.process_one()
        server=alina.ThreadingHTTPServer(('127.0.0.1',0),alina.Handler)
        old_port,old_url=alina.PORT,alina.URL
        alina.PORT=server.server_port;alina.URL=f'http://127.0.0.1:{alina.PORT}'
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        try:
            from urllib.parse import quote
            with urlopen(alina.URL+'/api/search?q='+quote('информация')) as response:
                self.assertEqual(len(json.load(response)),1)
            with self.assertRaises(HTTPError):
                urlopen(Request(alina.URL+'/api/pause',method='POST'))
            request=Request(alina.URL+'/api/pause',method='POST',headers={'X-Alina-Token':alina.TOKEN,'Origin':alina.URL})
            with urlopen(request) as response:self.assertTrue(json.load(response)['ok'])
            self.assertTrue(alina.snapshot()['paused'])
        finally:
            server.shutdown();server.server_close();thread.join()
            alina.PORT,alina.URL=old_port,old_url


if __name__=='__main__':unittest.main()
