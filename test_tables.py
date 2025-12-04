# test_tables.py
from database import SessionLocal
from models import Staff

db = SessionLocal()

# Insert test data (use basic_salary & bonus_percentage names)
new_staff = Staff(name="Test User", age=25, department="IT", basic_salary=50000, bonus_percentage=5)
db.add(new_staff)
db.commit()

# Fetch all rows
staff_list = db.query(Staff).all()
for staff in staff_list:
    print(staff.id, staff.name, staff.age, staff.basic_salary, staff.bonus_percentage, staff.department)

db.close()
