"""Read-only local datastore/schema discovery for ALINA C0.2.
Scans metadata and SQLite schemas only. Does not read document bodies or .env secrets.
"""
from __future__ import annotations
import argparse, hashlib, json, os, sqlite3
from pathlib import Path
SKIP={".git",".venv","venv","node_modules","__pycache__",".runtime","models","model","weights","checkpoints"}
DB_EXT={".db",".sqlite",".sqlite3"}
META_NAMES={"docker-compose.yml","docker-compose.yaml","compose.yml","compose.yaml"}
META_EXT={".sql"}
def sha256(p):
    h=hashlib.sha256()
    try:
        with p.open("rb") as f:
            for b in iter(lambda:f.read(1024*1024),b""): h.update(b)
        return h.hexdigest()
    except Exception:return None
def sqlite_schema(p):
    out={"tables":[],"indexes":[],"foreign_keys":[],"error":None}
    try:
        uri="file:"+p.resolve().as_posix()+"?mode=ro"
        con=sqlite3.connect(uri,uri=True,timeout=2)
        cur=con.cursor()
        for name,typ in cur.execute("select name,type from sqlite_master where type in ('table','view') and name not like 'sqlite_%' order by name"):
            cols=[{"name":r[1],"type":r[2],"notnull":bool(r[3]),"pk":bool(r[5])} for r in cur.execute('pragma table_info("'+name.replace('"','""')+'")').fetchall()]
            fks=[{"from":r[3],"to_table":r[2],"to":r[4]} for r in cur.execute('pragma foreign_key_list("'+name.replace('"','""')+'")').fetchall()]
            out["tables"].append({"name":name,"type":typ,"columns":cols})
            out["foreign_keys"] += [{"table":name,**x} for x in fks]
        out["indexes"]=[r[0] for r in cur.execute("select name from sqlite_master where type='index' and name not like 'sqlite_%' order by name")]
        con.close()
    except Exception as e: out["error"]=type(e).__name__+": "+str(e)[:300]
    return out
def walk(root):
    root=Path(root)
    for base,dirs,files in os.walk(root,followlinks=False):
        dirs[:]=[d for d in dirs if d.lower() not in SKIP]
        for fn in files:
            p=Path(base)/fn
            low=fn.lower()
            if p.suffix.lower() in DB_EXT or p.suffix.lower() in META_EXT or low in META_NAMES:
                yield p
def main():
    ap=argparse.ArgumentParser()
    ap.add_argument("roots",nargs="+")
    ap.add_argument("-o","--output",default="alina_c0_local_inventory.json")
    a=ap.parse_args()
    items=[]
    for root in a.roots:
        for p in walk(root):
            try: size=p.stat().st_size
            except OSError: continue
            item={"path":str(p),"size":size,"sha256":sha256(p),"kind":"sqlite" if p.suffix.lower() in DB_EXT else "schema_or_compose"}
            if item["kind"]=="sqlite": item["schema"]=sqlite_schema(p)
            items.append(item)
    result={"schema_version":"1.0","mode":"read_only_metadata_and_schema","roots":a.roots,"items":items,
            "notes":[".env files are not read","document bodies are not read","SQLite opened read-only","model/weight directories skipped"]}
    Path(a.output).write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding="utf-8")
    print(f"Wrote {a.output}: {len(items)} artifacts")
if __name__=="__main__": main()
