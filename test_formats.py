from pathlib import Path
import tempfile
import unittest
import zipfile
from extract import extract


class FormatTests(unittest.TestCase):
    def test_mhtml_word_unicode(self):
        from email.message import EmailMessage
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'archive.doc'
            message = EmailMessage()
            message.set_content('<html><p>Требование</p></html>'.encode('utf-16'), maintype='text', subtype='html', cte='base64')
            message.replace_header('Content-Type', 'text/html; charset="unicode"')
            p.write_bytes(message.as_bytes())
            # Real Word MHTML starts with MIME-Version and contains HTML MIME parts.
            raw = p.read_bytes()
            p.write_bytes(b'MIME-Version: 1.0\n' + raw)
            self.assertEqual(extract(p)['chunks'][0]['text'], 'Требование')

    def test_scanned_pdf_ocr_preserves_page_and_partial(self):
        from unittest.mock import patch
        from pypdf import PdfWriter
        with tempfile.TemporaryDirectory() as d:
            p = Path(d)/'scan.pdf'
            writer = PdfWriter()
            writer.add_blank_page(width=200, height=200)
            writer.write(p)
            with patch('ocr.recognize_pdf', return_value=([('страница 1; OCR — требуется сверка', 'Распознано')], True)):
                result = extract(p)
            self.assertEqual(result['status'], 'partial')
            self.assertIn('OCR', result['chunks'][0]['locator'])

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
