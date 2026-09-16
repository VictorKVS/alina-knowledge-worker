"""PDF page batches with transactional, persistent continuation in the worker."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import time


def extract_batch(path, start, sha):
    import pypdfium2 as pdfium
    if not sha:
        with open(path, 'rb') as source:
            sha = hashlib.file_digest(source, 'sha256').hexdigest()
    parts = []
    scanned = []
    with pdfium.PdfDocument(str(path)) as pdf:
        total = len(pdf)
        end = min(start + 8, total)
        for index in range(start, end):
            page = pdf[index]
            try:
                textpage = page.get_textpage()
                try: text = textpage.get_text_range()
                finally: textpage.close()
            finally: page.close()
            if text.strip(): parts.append((index, f'страница {index+1}', text))
            else: scanned.append(index)
    if scanned:
        from ocr import recognize_pdf
        recognized, incomplete = recognize_pdf(path, scanned)
        if incomplete: raise ValueError('OCR не завершил порцию; сохранённая позиция не изменена')
        parts.extend((int(loc.split()[1].rstrip(';'))-1, loc, text) for loc,text in recognized)
    chunks = []
    for _, locator, text in sorted(parts):
        for offset in range(0, len(text), 2500):
            piece = text[offset:offset+2500].strip()
            if piece: chunks.append({'locator':f'{locator}; фрагмент {offset//2500+1}', 'text':piece})
    return {'sha':sha, 'next':end, 'total':total, 'chunks':chunks}


def process(app, row):
    path = row['path']
    started = time.monotonic()
    with app.connection() as db:
        db.execute('CREATE TABLE IF NOT EXISTS pdf_progress(path TEXT PRIMARY KEY, size INTEGER, stamp INTEGER, sha TEXT, next INTEGER, total INTEGER)')
        progress = db.execute('SELECT * FROM pdf_progress WHERE path=?', (path,)).fetchone()
    valid = progress and progress['size']==row['size'] and progress['stamp']==row['stamp']
    start,sha = (progress['next'],progress['sha']) if valid else (0,'')
    app.LIVE.update(page=start, pages=progress['total'] if valid else None)
    output = app.DATA/'pdf-batch.json'
    try:
        output.unlink(missing_ok=True)
        proc = subprocess.run([sys.executable,'-B',str(Path(__file__)),path,str(start),sha,str(output)],
            capture_output=True,timeout=90,creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        result = json.loads(output.read_text('utf-8')) if output.exists() else {}
        if proc.returncode or 'error' in result: raise ValueError(result.get('error','Ошибка PDF-процесса'))
        stat = Path(path).stat()
        if (stat.st_size,stat.st_mtime_ns)!=(row['size'],row['stamp']): raise ValueError('Исходник изменился; требуется новый обход')
        sha = result['sha']
        complete = result['next']==result['total']
        with app.connection() as db:
            # A new extraction replaces old capped results only once; batches commit atomically.
            if start==0:
                db.execute('DELETE FROM chunks WHERE sha=?',(sha,))
                db.execute('DELETE FROM reading_notes WHERE sha=?',(sha,))
            for chunk in result['chunks']:
                db.execute('DELETE FROM chunks WHERE sha=? AND locator=?',(sha,chunk['locator']))
                db.execute('INSERT INTO chunks VALUES(?,?,?)',(sha,chunk['locator'],chunk['text']))
            count = db.execute('SELECT count(*) FROM chunks WHERE sha=?',(sha,)).fetchone()[0]
            status = 'ready' if complete and count else ('error' if complete else 'pending')
            detail = '' if status=='ready' else (f"Прочитано страниц: {result['next']} / {result['total']}; продолжение автоматически" if not complete else 'OCR завершён, но текст не обнаружен')
            db.execute('INSERT OR REPLACE INTO pdf_progress VALUES(?,?,?,?,?,?)',(path,row['size'],row['stamp'],sha,result['next'],result['total']))
            db.execute('INSERT OR REPLACE INTO versions VALUES(?,?,?)',(sha,'ready' if status=='ready' else 'partial',count))
            db.execute('UPDATE files SET sha=?,status=?,error=?,updated=?,duration=COALESCE(duration,0)+? WHERE path=?',(sha,status,detail,time.time(),time.monotonic()-started,path))
            db.execute('INSERT INTO events(at,kind,path,detail) VALUES(?,?,?,?)',(time.time(),'processed' if status=='ready' else ('error' if status=='error' else 'batch'),path,detail))
            app.study.add_notes(db,sha)
        app.LIVE.update(page=result['next'],pages=result['total'])
    except Exception as exc:
        with app.connection() as db:
            db.execute("UPDATE files SET status='error',error=?,updated=? WHERE path=?",(f'PDF: {exc}; позиция сохранена: страница {start}',time.time(),path))
            db.execute('INSERT INTO events(at,kind,path,detail) VALUES(?,?,?,?)',(time.time(),'error',path,str(exc)))
    finally: output.unlink(missing_ok=True)
    return True


if __name__=='__main__':
    try: result=extract_batch(sys.argv[1],int(sys.argv[2]),sys.argv[3])
    except Exception as exc:
        Path(sys.argv[4]).write_text(json.dumps({'error':str(exc)},ensure_ascii=False),encoding='utf-8')
        raise SystemExit(1)
    Path(sys.argv[4]).write_text(json.dumps(result,ensure_ascii=False),encoding='utf-8')
