from pathlib import Path
import tempfile
import unittest
import zipfile
from extract import extract


class FormatTests(unittest.TestCase):
    def test_fb2_encoding_nested_sections_notes_and_binary(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'source.fb2'
            p.write_bytes(('<?xml version="1.0" encoding="windows-1251"?>'
                '<FictionBook xmlns="http://www.gribuser.ru/xml/fictionbook/2.0">'
                '<body><section><title><p>Глава</p></title><section><p>Текст <emphasis>книги</emphasis>.</p></section></section></body>'
                '<body name="notes"><section><p>Примечание</p></section></body><binary>IGNORE</binary></FictionBook>').encode('cp1251'))
            chunks = extract(p)['chunks']
            self.assertEqual([c['text'] for c in chunks], ['Глава', 'Текст книги.', 'Примечание'])
            self.assertIn('body[2]', chunks[-1]['locator'])

    def test_doc_html_excludes_script(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'source.doc'
            p.write_text('<!DOCTYPE html><html><p>Требование &amp; проверка</p><script>hidden</script></html>', encoding='utf-8')
            r = extract(p)
            self.assertEqual(r['chunks'][0]['text'], 'Требование & проверка')
            self.assertIn('абзац', r['chunks'][0]['locator'])

    def test_rtf_unicode(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'source.rtf'
            p.write_bytes(br'{\rtf1\ansi\ansicpg1251\uc1 Hello \u1040?\par second}')
            text = '\n'.join(c['text'] for c in extract(p)['chunks'])
            self.assertIn('Hello А', text)
            self.assertIn('second', text)

    def test_epub_spine_order_and_locator(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'source.epub'
            with zipfile.ZipFile(p, 'w') as z:
                z.writestr('META-INF/container.xml', '<container><rootfiles><rootfile full-path="OEBPS/book.opf"/></rootfiles></container>')
                z.writestr('OEBPS/book.opf', '<package><manifest><item id="a" href="a.xhtml" media-type="application/xhtml+xml"/><item id="b" href="b.xhtml" media-type="application/xhtml+xml"/></manifest><spine><itemref idref="b"/><itemref idref="a"/></spine></package>')
                z.writestr('OEBPS/a.xhtml', '<p>Second</p>')
                z.writestr('OEBPS/b.xhtml', '<p>First</p>')
            r = extract(p)
            self.assertEqual([c['text'] for c in r['chunks']], ['First', 'Second'])
            self.assertIn('OEBPS/b.xhtml', r['chunks'][0]['locator'])

    def test_bad_epub_is_error(self):
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'bad.epub'
            p.write_bytes(b'broken')
            with self.assertRaises(zipfile.BadZipFile): extract(p)
