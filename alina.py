"""Alina: local, incremental knowledge-source preparation and honest progress reporting."""
import argparse
from contextlib import contextmanager
from datetime import datetime
import json
import os
from pathlib import Path
import secrets
import sqlite3
import subprocess
import sys
import threading
import time
import traceback
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse
from urllib.request import urlopen
import webbrowser
import study

BASE = Path(__file__).resolve().parent
DATA = BASE / 'data'
CONFIG_PATH = BASE / 'config.json'
if not CONFIG_PATH.exists():
    CONFIG_PATH = BASE / 'config.example.json'
CONFIG = json.loads(CONFIG_PATH.read_text(encoding='utf-8-sig'))
CONFIG['roots'] = [str((BASE / p).resolve()) if not Path(p).is_absolute() else p for p in CONFIG['roots']]
PORT = CONFIG['port']
URL = f'http://127.0.0.1:{PORT}'
TOKEN = secrets.token_urlsafe(32)
STOP = threading.Event()
SUPPORTED = {'.md', '.txt', '.json', '.yaml', '.yml', '.pdf', '.doc', '.rtf', '.epub', '.fb2'}
SKIP = {'.git', '.venv', 'venv', 'node_modules', '__pycache__', '.runtime', '_REPORTS'}
LIVE = {'phase': 'запуск', 'current': '', 'scan_error': '', 'last_scan': None, 'unsupported': 0}


@contextmanager
def connection():
    db = sqlite3.connect(DATA / 'alina.sqlite', timeout=30)
    db.row_factory = sqlite3.Row
    try:
        with db:
            yield db
    finally:
        db.close()


def init():
    DATA.mkdir(parents=True, exist_ok=True)
    with connection() as db:
        db.executescript('''
        PRAGMA journal_mode=WAL;
        CREATE TABLE IF NOT EXISTS files(path TEXT PRIMARY KEY, size INTEGER, stamp INTEGER,
          sha TEXT, status TEXT, error TEXT, updated REAL, duration REAL);
        CREATE TABLE IF NOT EXISTS versions(sha TEXT PRIMARY KEY, status TEXT, chunks INTEGER);
        CREATE VIRTUAL TABLE IF NOT EXISTS chunks USING fts5(sha UNINDEXED, locator UNINDEXED, text);
        CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY, at REAL, kind TEXT, path TEXT, detail TEXT);
        CREATE TABLE IF NOT EXISTS settings(key TEXT PRIMARY KEY,value TEXT);
        CREATE TABLE IF NOT EXISTS reports(id INTEGER PRIMARY KEY, at REAL, body TEXT);
        ''')
        db.execute('INSERT OR IGNORE INTO settings VALUES(?,?)', ('paused','false'))
        db.execute('INSERT OR IGNORE INTO settings VALUES(?,?)', ('active_seconds','0'))
        db.execute('INSERT OR IGNORE INTO settings VALUES(?,?)', ('report_baseline',json.dumps({'at':time.time(),'processed':0,'errors':0,'chunks':0})))
    with connection() as db:
        study.init(db)
        for row in db.execute("SELECT DISTINCT sha FROM files WHERE sha IS NOT NULL AND status IN ('ready','partial')").fetchall():
            study.add_notes(db,row[0])


def setting(key, value=None):
    with connection() as db:
        if value is not None:
            db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)', (key,str(value)))
        row = db.execute('SELECT value FROM settings WHERE key=?',(key,)).fetchone()
        return row[0] if row else None


def snapshot():
    with connection() as db:
        counts = dict(db.execute('SELECT status,count(*) FROM files GROUP BY status').fetchall())
        totals = dict(db.execute('SELECT kind,count(*) FROM events GROUP BY kind').fetchall())
        reports = [json.loads(r[0]) for r in db.execute('SELECT body FROM reports ORDER BY id DESC LIMIT 24')]
        errors = [dict(r) for r in db.execute("SELECT path,error,status FROM files WHERE status IN ('error','partial','oversize') ORDER BY updated DESC LIMIT 10")]
        chunk_count = db.execute('SELECT count(*) FROM chunks').fetchone()[0]
        study_status = study.summary(db)
    total = sum(counts.values())
    terminal = sum(counts.get(k,0) for k in ('ready','partial','error','oversize'))
    return {'name':'Алина', 'mode':'Локальная подготовка источников; не утверждение фактов в KB',
        'paused':setting('paused')=='true', 'counts':counts, 'total':total,
        'progress':round(100*terminal/total,1) if total else 0,
        'progress_label':'Обработано в текущем учёте (включая ошибки)',
        'processed':totals.get('processed',0), 'errors_total':totals.get('error',0),
        'chunks':chunk_count, 'active_seconds':float(setting('active_seconds') or 0),
        'live':dict(LIVE), 'reports':reports, 'errors':errors,
        'next_report':json.loads(setting('report_baseline'))['at']+CONFIG['report_seconds'],
        'roots':CONFIG['roots'], 'pid':os.getpid(), 'study':study_status}


def scan():
    found = []
    failures = []
    unsupported = 0
    catalog=[]
    for root in CONFIG['roots']:
        folder = Path(root)
        if not folder.is_dir():
            failures.append(f'Недоступен источник: {root}')
            continue
        for directory, dirs, names in os.walk(folder, onerror=lambda e: failures.append(str(e))):
            if STOP.is_set(): break
            dirs[:] = [d for d in dirs if d not in SKIP and not (Path(directory)/d).is_symlink()]
            for name in names:
                path = Path(directory)/name
                domain,kind=study.classify(path)
                catalog.append((str(path),domain,kind,int(path.suffix.lower() in SUPPORTED)))
                if path.suffix.lower() not in SUPPORTED:
                    unsupported += 1
                    continue
                # Library books can be file symlinks to originals. Read them as sources;
                # directory symlinks remain excluded above to prevent recursive traversal.
                try:
                    st = path.stat()
                    found.append((str(path), st.st_size, st.st_mtime_ns))
                except OSError as exc: failures.append(str(exc))
    with connection() as db:
        db.executemany('INSERT OR REPLACE INTO catalog VALUES(?,?,?,?)',catalog)
        for path,size,stamp in found:
            row = db.execute('SELECT size,stamp FROM files WHERE path=?',(path,)).fetchone()
            if not row or row['size'] != size or row['stamp'] != stamp:
                db.execute('INSERT INTO files VALUES(?,?,?,?,?,?,?,?) ON CONFLICT(path) DO UPDATE SET size=excluded.size,stamp=excluded.stamp,status=excluded.status,error=NULL',
                           (path,size,stamp,None,'pending',None,0,0))
        pending=db.execute("SELECT count(*) FROM files WHERE status='pending'").fetchone()[0]
        cycle_state=db.execute("SELECT value FROM settings WHERE key='study_cycle_state'").fetchone()[0]
        if pending and cycle_state=='waiting':
            db.execute("UPDATE settings SET value=CAST(value AS INTEGER)+1 WHERE key='study_cycle'")
            db.execute("UPDATE settings SET value='active' WHERE key='study_cycle_state'")
        db.execute("UPDATE settings SET value=CAST(value AS INTEGER)+1 WHERE key='scan_count'")
    LIVE.update(last_scan=time.time(), scan_error='; '.join(failures[:5]), unsupported=unsupported)


def process_one():
    with connection() as db:
        row = study.next_file(db)
        if not row:
            db.execute("UPDATE settings SET value='waiting' WHERE key='study_cycle_state'")
    if not row: return False
    path = Path(row['path'])
    domain,kind=study.classify(path)
    LIVE.update(phase='разбор документа', current=str(path),study_domain=study.DOMAINS[domain],source_kind=kind)
    started = time.monotonic()
    output = DATA / 'extract-result.json'
    status, error, sha, payload = 'error', '', None, None
    try:
        if row['size'] > CONFIG['max_file_bytes']:
            status, error = 'oversize', 'Файл больше 100 МБ: оставлен на отдельную обработку'
        else:
            output.unlink(missing_ok=True)
            proc = subprocess.run([sys.executable, '-B', str(BASE/'extract.py'),str(path),str(output)],
                timeout=CONFIG['extract_timeout_seconds'], capture_output=True,
                creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
            payload = json.loads(output.read_text(encoding='utf-8')) if output.exists() else {}
            if proc.returncode or 'error' in payload:
                raise ValueError(payload.get('error','Ошибка процесса извлечения'))
            st = path.stat()
            if st.st_size != row['size'] or st.st_mtime_ns != row['stamp']:
                raise ValueError('Документ изменился во время извлечения; будет перепроверен')
            sha, status = payload['sha256'],payload['status']
            if status == 'partial': error='Извлечена часть документа: достигнут предел страниц или текста'
    except subprocess.TimeoutExpired:
        error='Превышено время извлечения: 60 секунд'
    except Exception as exc:
        error=str(exc)[:1200]
    with connection() as db:
        if sha and not db.execute('SELECT 1 FROM versions WHERE sha=?',(sha,)).fetchone():
            db.executemany('INSERT INTO chunks VALUES(?,?,?)',[(sha,c['locator'],c['text']) for c in payload['chunks']])
            db.execute('INSERT INTO versions VALUES(?,?,?)',(sha,status,len(payload['chunks'])))
        db.execute('UPDATE files SET sha=?,status=?,error=?,updated=?,duration=? WHERE path=?',
                   (sha,status,error,time.time(),time.monotonic()-started,str(path)))
        db.execute('INSERT INTO events(at,kind,path,detail) VALUES(?,?,?,?)',
                   (time.time(),'processed' if status in ('ready','partial') else 'error',str(path),status))
        study.add_notes(db,sha)
    output.unlink(missing_ok=True)
    return True


def make_report(notify=True):
    old = json.loads(setting('report_baseline'))
    current = snapshot()
    stamp = time.time()
    body = {'at':stamp,'since':old['at'],'before':old,
        'after':{'processed':current['processed'],'errors':current['errors_total'],'chunks':current['chunks']},
        'delta':{'processed':current['processed']-old['processed'],'errors':current['errors_total']-old['errors'],
                 'chunks':current['chunks']-old['chunks']}, 'progress':current['progress'],
        'pending':current['counts'].get('pending',0),'active_seconds':current['active_seconds'],
        'paused':current['paused'],'phase':current['live']['phase'], 'scan_error':current['live']['scan_error'],
        'study':current['study']}
    with connection() as db:
        db.execute('INSERT INTO reports(at,body) VALUES(?,?)',(stamp,json.dumps(body,ensure_ascii=False)))
        db.execute('INSERT OR REPLACE INTO settings VALUES(?,?)',('report_baseline',json.dumps({'at':stamp,**body['after']})))
    report_path = DATA/'latest-report.json'
    report_path.write_text(json.dumps(body,ensure_ascii=False),encoding='utf-8')
    if notify:
        subprocess.Popen(['powershell.exe','-NoProfile','-WindowStyle','Hidden','-File',str(BASE/'notify.ps1'),
                          '-ReportPath',str(report_path),'-DashboardUrl',URL],
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
    return body


def worker():
    last_scan=0
    tick=time.monotonic()
    while not STOP.is_set():
        try:
            paused=setting('paused')=='true'
            if paused: LIVE.update(phase='пауза',current='')
            else:
                if time.monotonic()-last_scan >= CONFIG['scan_seconds']:
                    LIVE['phase']='поиск новых документов'
                    scan(); last_scan=time.monotonic()
                if not process_one():
                    LIVE.update(phase='ожидание новых документов',current='')
            delta=time.monotonic()-tick; tick=time.monotonic()
            setting('active_seconds',float(setting('active_seconds') or 0)+delta)
            if time.time()-json.loads(setting('report_baseline'))['at'] >= CONFIG['report_seconds']:
                make_report()
        except Exception:
            LIVE.update(phase='ошибка — повтор через 5 секунд',scan_error=traceback.format_exc()[-1000:])
            with (DATA/'worker.log').open('a',encoding='utf-8') as f: f.write(traceback.format_exc()+'\n')
            STOP.wait(5)
        STOP.wait(0.15 if LIVE['phase']=='разбор документа' else 2)


class Handler(BaseHTTPRequestHandler):
    def log_message(self,*args): pass
    def send(self,body,status=200,kind='application/json; charset=utf-8'):
        raw=body if isinstance(body,bytes) else json.dumps(body,ensure_ascii=False).encode()
        self.send_response(status); self.send_header('Content-Type',kind)
        self.send_header('Cache-Control','no-store'); self.send_header('X-Content-Type-Options','nosniff')
        self.send_header('Content-Length',str(len(raw))); self.end_headers(); self.wfile.write(raw)
    def valid_host(self): return self.headers.get('Host') in {f'127.0.0.1:{PORT}',f'localhost:{PORT}'}
    def do_GET(self):
        if not self.valid_host(): return self.send({'error':'host'},403)
        u=urlparse(self.path)
        if u.path=='/':
            page=(BASE/'dashboard.html').read_text(encoding='utf-8').replace('__TOKEN__',TOKEN)
            return self.send(page.encode(),kind='text/html; charset=utf-8')
        if u.path=='/api/status': return self.send(snapshot())
        if u.path=='/study-ui.js':
            return self.send((BASE/'study-ui.js').read_bytes(),kind='text/javascript; charset=utf-8')
        if u.path=='/api/books':
            domain=parse_qs(u.query).get('domain',['security'])[0]
            if domain not in study.DOMAINS: return self.send({'error':'domain'},400)
            with connection() as db: result=study.book_results(db,domain)
            return self.send(result)
        if u.path=='/api/search':
            q=parse_qs(u.query).get('q',[''])[0][:200]
            terms=[f'"{s.replace(chr(34),chr(34)*2)}"' for s in q.split()[:8]]
            if not terms: return self.send([])
            with connection() as db:
                rows=db.execute("SELECT c.locator,substr(c.text,1,700) excerpt,f.path FROM chunks c JOIN files f ON f.sha=c.sha WHERE chunks MATCH ? AND f.status IN ('ready','partial') LIMIT 15",(' AND '.join(terms),)).fetchall()
            return self.send([dict(r) for r in rows])
        return self.send({'error':'not found'},404)
    def do_POST(self):
        if (not self.valid_host() or self.headers.get('X-Alina-Token')!=TOKEN
            or self.headers.get('Origin') not in {URL,f'http://localhost:{PORT}'}):
            return self.send({'error':'forbidden'},403)
        if self.path.startswith('/api/focus/'):
            domain=self.path.rsplit('/',1)[-1]
            if domain not in {'auto',*study.DOMAINS}: return self.send({'error':'domain'},400)
            setting('focus_domain',domain)
        elif self.path.startswith('/api/retry/'):
            domain=self.path.rsplit('/',1)[-1]
            if domain not in study.DOMAINS: return self.send({'error':'domain'},400)
            with connection() as db:
                db.execute("UPDATE files SET status='pending' WHERE status='error' AND path IN (SELECT path FROM catalog WHERE domain=?)",(domain,))
        elif self.path=='/api/pause': setting('paused','true')
        elif self.path=='/api/resume': setting('paused','false')
        else: return self.send({'error':'not found'},404)
        return self.send({'ok':True})


def serve():
    init()
    try: server=ThreadingHTTPServer(('127.0.0.1',PORT),Handler)
    except OSError: return 17
    thread=threading.Thread(target=worker,daemon=True); thread.start()
    try: server.serve_forever(poll_interval=1)
    finally: STOP.set(); server.server_close()
    return 0


def open_dashboard():
    try:
        with urlopen(URL+'/api/status',timeout=2) as r: json.load(r)
    except Exception:
        subprocess.Popen(['powershell.exe','-NoProfile','-WindowStyle','Hidden','-File',str(BASE/'supervisor.ps1')],
                         creationflags=getattr(subprocess,'CREATE_NO_WINDOW',0))
        for _ in range(30):
            try:
                with urlopen(URL+'/api/status',timeout=1): break
            except Exception: time.sleep(0.5)
    webbrowser.open(URL)


if __name__=='__main__':
    parser=argparse.ArgumentParser(); parser.add_argument('--serve',action='store_true'); parser.add_argument('--open',action='store_true')
    args=parser.parse_args()
    if args.open: open_dashboard()
    else: raise SystemExit(serve())
