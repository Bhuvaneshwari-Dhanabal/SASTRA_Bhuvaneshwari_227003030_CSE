from app.database import get_db

# Get the connection/session
db = get_db()

print('Tables and row counts:')
# Query to fetch all user table names
tables = [r[0] for r in db.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%'").fetchall()]

for t in tables:
    count = db.execute(f'SELECT COUNT(*) FROM "{t}"').fetchone()[0]
    print(f"{t}: {count}")

db.close()
