"""Bounded offline Windows OCR; returned text must be verified against source."""
from pathlib import Path
import subprocess
import tempfile


def recognize_pdf(path, pages):
    import pypdfium2 as pdfium
    selected = pages[:12]
    with tempfile.TemporaryDirectory(prefix='alina-ocr-') as folder:
        with pdfium.PdfDocument(str(path)) as pdf:
            for index in selected:
                page = pdf[index]
                try:
                    scale = min(2, 2400 / max(page.get_size()))
                    bitmap = page.render(scale=scale)
                    try: bitmap.to_pil().convert('RGB').save(Path(folder)/f'{index:06}.png')
                    finally: bitmap.close()
                finally: page.close()
        try:
            proc = subprocess.run(['powershell.exe', '-NoProfile', '-NonInteractive', '-ExecutionPolicy', 'Bypass',
                '-File', str(Path(__file__).with_name('ocr.ps1')), '-InputFolder', folder],
                capture_output=True, timeout=35, creationflags=getattr(subprocess, 'CREATE_NO_WINDOW', 0))
            if proc.returncode:
                raise ValueError('Windows OCR: ' + proc.stderr.decode('utf-8', errors='replace')[-800:])
        except subprocess.TimeoutExpired:
            pass  # Completed pages survive until read below; unfinished pages mark partial.
        parts = []
        completed = 0
        for index in selected:
            output = Path(folder)/f'{index:06}.png.txt'
            if output.exists():
                completed += 1
                text = output.read_text(encoding='utf-8-sig').strip()
                if text: parts.append((f'страница {index+1}; OCR — требуется сверка', text))
        return parts, completed < len(pages)
