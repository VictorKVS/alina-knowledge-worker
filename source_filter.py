"""Keep Office lock files out of the source catalog, including older workers."""
def install(db):
    for table in ('files', 'catalog'):
        db.execute(f'''CREATE TRIGGER IF NOT EXISTS ignore_lock_{table}
          BEFORE INSERT ON {table}
          WHEN replace(NEW.path, char(92), '/') LIKE '%/~$%'
          BEGIN SELECT RAISE(IGNORE); END''')
        db.execute(f"DELETE FROM {table} WHERE replace(path,char(92),'/') LIKE '%/~$%'")
