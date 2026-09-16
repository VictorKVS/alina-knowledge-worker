"""Bounded text extraction in a killable child process; never executes source content."""
import hashlib
import json
from pathlib import Path
import sys


def extract(path):
    path = Path(path)
    raw = path.read_bytes()
    parts = []
    partial = False
    if path.suffix.lower() == '.pdf':
        from pypdf import PdfReader
        import io
        reader = PdfReader(io.BytesIO(raw))
        if reader.is_encrypted and not reader.decrypt(''):
            raise ValueError('PDF зашифрован')
        partial = len(reader.pages) > 2000
        for i, page in enumerate(reader.pages[:2000]):
            text = page.extract_text() or ''
            if text.strip():
                parts.append((f'страница {i+1}', text))
        if not parts:
            raise ValueError('Нет извлекаемого текста: требуется OCR')
    elif path.suffix.lower() in {'.doc', '.rtf', '.epub', '.fb2'}:
        from formats import document_parts
        parts = document_parts(path, raw)
    else:
        text = raw.decode('utf-8-sig', errors='strict')
        lines = text.splitlines()
        parts = [(f'строки {i+1}–{min(i+24,len(lines))}', '\n'.join(lines[i:i+24])) for i in range(0,len(lines),24)]
    chunks = []
    size = 0
    for locator, text in parts:
        for start in range(0, len(text), 2500):
            chunk = text[start:start+2500].strip()
            if not chunk:
                continue
            size += len(chunk)
            if size > 5_000_000:
                partial = True
                break
            chunks.append({'locator': locator + f'; фрагмент {start//2500+1}', 'text': chunk})
        if size > 5_000_000:
            break
    if not chunks:
        raise ValueError('Нет непустых текстовых фрагментов')
    return {'sha256': hashlib.sha256(raw).hexdigest(), 'chunks': chunks,
            'status': 'partial' if partial else 'ready', 'bytes': len(raw)}


if __name__ == '__main__':
    try:
        result = extract(sys.argv[1])
        Path(sys.argv[2]).write_text(json.dumps(result, ensure_ascii=False), encoding='utf-8')
    except Exception as exc:
        Path(sys.argv[2]).write_text(json.dumps({'error': f'{type(exc).__name__}: {exc}'}, ensure_ascii=False), encoding='utf-8')
        raise SystemExit(1)
