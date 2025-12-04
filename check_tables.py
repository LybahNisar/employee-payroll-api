# check_tables.py
from database import SessionLocal
from sqlalchemy import text

db = SessionLocal()
try:
    result = db.execute(text("SELECT table_name FROM information_schema.tables WHERE table_schema='public';"))
    print("Tables in the 'public' schema:")
    for row in result:
        print(row[0])
finally:
    db.close()
