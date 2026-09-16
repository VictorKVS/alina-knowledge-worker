"""Local document readers. No network requests or source execution."""
from html.parser import HTMLParser
from pathlib import Path, PurePosixPath
import posixpath
import subprocess
import tempfile
from urllib.parse import unquote
import xml.etree.ElementTree as ET
import zipfile


class TextHTML(HTMLParser):
    def __init__(self):
        super().__init__(convert_charrefs=True)
        self.parts = []
        self.hidden = 0

    def handle_starttag(self, tag, attrs):
        if tag in ('script', 'style'): self.hidden += 1
        if tag in ('p', 'div', 'br', 'h1', 'h2', 'li', 'tr'): self.parts.append('\n')

    def handle_endtag(self, tag):
        if tag in ('script', 'style'): self.hidden = max(0, self.hidden - 1)
        if tag in ('p', 'div', 'li', 'td'): self.parts.append('\n')

    def handle_data(self, data):
        if not self.hidden: self.parts.append(data)


def html_text(raw):
    try: text = raw.decode('utf-8-sig')
    except UnicodeDecodeError: text = raw.decode('cp1251')
    parser = TextHTML()
    parser.feed(text)
    return '\n'.join(line.strip() for line in ''.join(parser.parts).splitlines() if line.strip())


def epub_parts(path):
    with zipfile.ZipFile(path) as archive:
        if sum(i.file_size for i in archive.infolist()) > 200_000_000:
            raise ValueError('EPUB: распакованный объём больше 200 МБ')
        container = ET.fromstring(archive.read('META-INF/container.xml'))
        roots = container.findall('.//{*}rootfile')
        if not roots: raise ValueError('EPUB: отсутствует пакет книги')
        opf = roots[0].attrib['full-path']
        root = ET.fromstring(archive.read(opf))
        manifest = {e.attrib['id']: e.attrib for e in root.findall('.//{*}manifest/{*}item')}
        parts = []
        for n, item in enumerate(root.findall('.//{*}spine/{*}itemref'), 1):
            entry = manifest[item.attrib['idref']]
            if entry.get('media-type') not in ('application/xhtml+xml', 'text/html'):
                raise ValueError('EPUB: неподдерживаемый раздел ' + entry.get('media-type', ''))
            name = posixpath.normpath(str(PurePosixPath(opf).parent / unquote(entry['href'].split('#')[0])))
            parts.append((f'раздел {n}: {name}', html_text(archive.read(name))))
        return parts


def office_text(path, format):
    with tempfile.TemporaryDirectory(prefix='alina-office-') as folder:
        out = Path(folder) / 'text.txt'
        pid_file = Path(folder) / 'word.pid'
        command = ['powershell.exe', '-NoProfile', '-NonInteractive', '-STA', '-ExecutionPolicy', 'Bypass',
                   '-File', str(Path(__file__).with_name('office-text.ps1')),
                   '-Source', str(Path(path).resolve()), '-Output', str(out), '-PidFile', str(pid_file), '-Format', format]
        timed_out = False
        try:
            result = subprocess.run(command, capture_output=True, timeout=40,
                                    creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if result.returncode or not out.exists():
                raise ValueError('Не удалось прочитать документ: ' + result.stderr.decode('utf-8', errors='replace')[-1200:])
            return out.read_text(encoding='utf-8-sig')
        except subprocess.TimeoutExpired:
            timed_out = True
            raise
        finally:
            if timed_out and pid_file.exists():
                word_pid = int(pid_file.read_text())
                subprocess.run(['taskkill', '/PID', str(word_pid), '/F'], capture_output=True, timeout=5,
                               creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))


def fb2_parts(raw):
    root = ET.fromstring(raw)
    if root.tag.split('}')[-1] != 'FictionBook':
        raise ValueError('FB2: отсутствует FictionBook')
    parts = []
    blocks = {'p', 'v', 'subtitle', 'text-author', 'date', 'td', 'th'}
    def walk(node, locator):
        tag = node.tag.split('}')[-1]
        if tag in ('binary', 'image'): return
        if tag in blocks:
            text = ''.join(node.itertext()).strip()
            if text: parts.append((locator, text))
            return
        for index, child in enumerate(node, 1):
            walk(child, locator + '/' + child.tag.split('}')[-1] + f'[{index}]')
    for index, body in enumerate(root.findall('{*}body'), 1):
        walk(body, f'FB2 body[{index}]')
    return parts


def document_parts(path, raw):
    suffix = path.suffix.lower()
    if suffix == '.epub': return epub_parts(path)
    if suffix == '.fb2': return fb2_parts(raw)
    if raw.lstrip().lower().startswith(b'mime-version:'):
        from email.parser import BytesParser
        from email import policy
        message = BytesParser(policy=policy.default).parsebytes(raw)
        texts = []
        for part in message.walk():
            if part.get_content_type() == 'text/html':
                content = part.get_payload(decode=True)
                if content:
                    charset = part.get_content_charset() or 'utf-8'
                    if charset.lower() == 'unicode': charset = 'utf-16'
                    decoded = content.decode(charset)
                    texts.append(html_text(decoded.encode('utf-8')))
        if not texts: raise ValueError('MHTML: не найден HTML-текст')
        text = '\n'.join(texts)
    elif raw.lstrip().startswith(b'{\\rtf'):
        text = office_text(path, 'rtf')
    elif raw.lstrip().lower().startswith((b'<!doctype html', b'<html')):
        text = html_text(raw)
    elif suffix == '.doc' and raw.startswith(bytes.fromhex('d0cf11e0a1b11ae1')):
        text = office_text(path, 'doc')
    else:
        raise ValueError('Содержимое не соответствует поддерживаемому DOC/RTF')
    return [('текст документа; абзац ' + str(n), paragraph) for n, paragraph in enumerate(text.splitlines(), 1) if paragraph.strip()]
