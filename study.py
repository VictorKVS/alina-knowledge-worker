"""Folder-based study routing and traceable reading excerpts, not trained model weights."""
import hashlib
import json
import time

DOMAINS = {'security':'Информационная безопасность', 'design':'Проектирование',
           'architecture':'Архитектура систем', 'other':'Остальная библиотека'}


def classify(path):
    parts = set(str(path).replace('\\','/').casefold().split('/'))
    book = 'father_golden_library' in parts and '_non_book_documents' not in parts
    if parts & {'12_security','00_standards','19_standards_governance','security-knowledge','security-corpora','security-core','application-security','devsecops'}:
        domain='security'
    elif parts & {'01_requirements_analysis','02_domain_model_ddd','06_api_integration','09_software_engineering','programming-practice'}:
        domain='design'
    elif parts & {'04_software_architecture','08_microservices_distributed','07_data_knowledge_graph','11_observability_reliability','architecture','distributed-systems'}:
        domain='architecture'
    else: domain='other'
    return domain, 'book' if book else 'reference'


def init(db):
    db.executescript('''
    CREATE TABLE IF NOT EXISTS catalog(path TEXT PRIMARY KEY,domain TEXT,kind TEXT,supported INTEGER);
    CREATE TABLE IF NOT EXISTS reading_notes(id TEXT PRIMARY KEY,sha TEXT,locator TEXT,excerpt TEXT,created REAL);
    ''')
    for key,value in [('focus_domain','auto'),('study_cycle','1'),('study_cycle_state','active'),('scan_count','0')]:
        db.execute('INSERT OR IGNORE INTO settings VALUES(?,?)',(key,value))
    for row in db.execute('SELECT path FROM files').fetchall():
        domain,kind=classify(row[0])
        db.execute('INSERT OR IGNORE INTO catalog VALUES(?,?,?,1)',(row[0],domain,kind))


def add_notes(db,sha):
    if not sha or not db.execute("SELECT 1 FROM files f JOIN catalog c ON c.path=f.path WHERE f.sha=? AND c.kind='book' AND f.status IN ('ready','partial')",(sha,)).fetchone():
        return
    # Mechanical excerpts retain exact source wording. They are not conclusions or verified ideas.
    rows=db.execute('SELECT locator,text FROM chunks WHERE sha=? ORDER BY rowid LIMIT 5',(sha,)).fetchall()
    for row in rows:
        ident=hashlib.sha256((sha+'\0'+row[0]).encode()).hexdigest()
        db.execute('INSERT OR IGNORE INTO reading_notes VALUES(?,?,?,?,?)',(ident,sha,row[0],row[1][:1200],time.time()))


def next_file(db):
    focus=db.execute("SELECT value FROM settings WHERE key='focus_domain'").fetchone()[0]
    return db.execute('''SELECT f.* FROM files f JOIN catalog c ON c.path=f.path WHERE f.status='pending'
      ORDER BY CASE WHEN c.domain=? THEN 0 ELSE 1 END,
      CASE WHEN c.kind='book' THEN 0 ELSE 1 END,
      CASE c.domain WHEN 'security' THEN 0 WHEN 'design' THEN 1 WHEN 'architecture' THEN 2 ELSE 3 END,
      f.size,f.path LIMIT 1''',(focus,)).fetchone()


def summary(db):
    tracks=[]
    for domain,title in DOMAINS.items():
        rows=db.execute('''SELECT c.kind,c.supported,COALESCE(f.status,CASE WHEN c.supported=0 THEN 'unsupported' ELSE 'unavailable' END) status,count(*) n
          FROM catalog c LEFT JOIN files f ON f.path=c.path WHERE c.domain=? GROUP BY c.kind,c.supported,f.status''',(domain,)).fetchall()
        books=sum(r['n'] for r in rows if r['kind']=='book')
        ready=sum(r['n'] for r in rows if r['kind']=='book' and r['status']=='ready')
        pending=sum(r['n'] for r in rows if r['kind']=='book' and r['status']=='pending')
        attention=sum(r['n'] for r in rows if r['kind']=='book' and r['status'] in ('error','partial','oversize','unsupported','unavailable'))
        hashes=[r[0] for r in db.execute("SELECT DISTINCT f.sha FROM files f JOIN catalog c ON c.path=f.path WHERE c.domain=? AND c.kind='book' AND f.status IN ('ready','partial') AND f.sha IS NOT NULL",(domain,))]
        chunks=sum(db.execute('SELECT chunks FROM versions WHERE sha=?',(h,)).fetchone()[0] for h in hashes)
        notes=sum(db.execute('SELECT count(*) FROM reading_notes WHERE sha=?',(h,)).fetchone()[0] for h in hashes)
        tracks.append({'id':domain,'title':title,'books':books,'ready':ready,'pending':pending,'attention':attention,
            'references':sum(r['n'] for r in rows if r['kind']=='reference'), 'chunks':chunks,'notes':notes,
            'progress':round(100*ready/books,1) if books else 0})
    upcoming=next_file(db)
    return {'tracks':tracks,'next':dict(upcoming) if upcoming else None,
        'cycle':int(db.execute("SELECT value FROM settings WHERE key='study_cycle'").fetchone()[0]),
        'cycle_state':db.execute("SELECT value FROM settings WHERE key='study_cycle_state'").fetchone()[0],
        'scans':int(db.execute("SELECT value FROM settings WHERE key='scan_count'").fetchone()[0]),
        'focus':db.execute("SELECT value FROM settings WHERE key='focus_domain'").fetchone()[0],
        'method':'Порядок по разделам библиотеки. Выдержки требуют содержательного разбора и проверки.'}


def book_results(db,domain):
    if domain not in DOMAINS: raise ValueError('Unknown domain')
    books=[dict(r) for r in db.execute('''SELECT f.path,f.sha,f.status,f.error,f.duration,COALESCE(v.chunks,0) chunks
      FROM catalog c JOIN files f ON f.path=c.path LEFT JOIN versions v ON v.sha=f.sha
      WHERE c.domain=? AND c.kind='book' ORDER BY f.updated DESC,f.path LIMIT 15''',(domain,))]
    for book in books:
        book['notes']=[dict(r) for r in db.execute('SELECT locator,excerpt FROM reading_notes WHERE sha=? ORDER BY created,id LIMIT 3',(book['sha'],))] if book['status'] in ('ready','partial') else []
    unsupported=[r[0] for r in db.execute("SELECT path FROM catalog WHERE domain=? AND kind='book' AND supported=0 ORDER BY path LIMIT 10",(domain,))]
    return {'books':books,'unsupported':unsupported}
