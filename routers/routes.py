# routers/routes.py
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from datetime import timedelta
from database import get_db
import schemas
from models import User, Staff
import auth

router = APIRouter(tags=["API"])

# ------------------ AUTHENTICATION ------------------

@router.post("/auth/signup")
def signup(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    existing_user = db.query(User).filter(User.username == user_in.username).first()
    if existing_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Username already exists")

    hashed_pwd = auth.hash_password(user_in.password)
    new_user = User(username=user_in.username, hashed_password=hashed_pwd)
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {
        "message": "Signup successful!",
        "user": {
            "id": new_user.id,
            "username": new_user.username,
            "is_active": new_user.is_active
        }
    }

@router.post("/auth/login", response_model=schemas.Token)
def login(user_in: schemas.UserCreate, db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == user_in.username).first()
    if not user or not auth.verify_password(user_in.password, user.hashed_password):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Invalid username or password")

    access_token = auth.create_access_token(
        data={"user_id": user.id, "username": user.username},
        expires_delta=timedelta(hours=1)
    )
    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/auth/profile", response_model=schemas.UserOut)
def get_profile(payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    user_id = payload.get("user_id")
    user = db.query(User).filter(User.id == user_id).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    return user

# ------------------ STAFF / EMPLOYEE CRUD ------------------

# Helper to calculate bonus_percentage and final_salary
def calculate_bonus_and_salary(basic_salary: float, bonus_amount: float):
    bonus_percentage = (bonus_amount / basic_salary * 100) if basic_salary else 0
    final_salary = basic_salary + bonus_amount
    return bonus_percentage, final_salary

# Create Staff
@router.post("/staff", response_model=schemas.StaffOut)
def create_staff(staff_in: schemas.StaffCreate, payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    bonus_percentage, final_salary = calculate_bonus_and_salary(staff_in.basic_salary, staff_in.bonus_amount)
    new_staff = Staff(
        name=staff_in.name,
        age=staff_in.age,
        department=staff_in.department,
        basic_salary=staff_in.basic_salary,
        bonus_percentage=bonus_percentage
    )
    db.add(new_staff)
    db.commit()
    db.refresh(new_staff)

    return schemas.StaffOut(
        id=new_staff.id,
        name=new_staff.name,
        age=new_staff.age,
        department=new_staff.department,
        basic_salary=new_staff.basic_salary,
        bonus_percentage=bonus_percentage,
        bonus_amount=staff_in.bonus_amount,
        final_salary=final_salary
    )

# Get all Staff
@router.get("/staff", response_model=list[schemas.StaffOut])
def get_all_staff(payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    staff_list = db.query(Staff).all()
    result = []
    for s in staff_list:
        bonus_amount = s.basic_salary * s.bonus_percentage / 100
        final_salary = s.basic_salary + bonus_amount
        result.append(schemas.StaffOut(
            id=s.id,
            name=s.name,
            age=s.age,
            department=s.department,
            basic_salary=s.basic_salary,
            bonus_percentage=s.bonus_percentage,
            bonus_amount=bonus_amount,
            final_salary=final_salary
        ))
    return result

# Get single Staff
@router.get("/staff/{staff_id}", response_model=schemas.StaffOut)
def get_staff(staff_id: int, payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    s = db.query(Staff).filter(Staff.id == staff_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    bonus_amount = s.basic_salary * s.bonus_percentage / 100
    final_salary = s.basic_salary + bonus_amount
    return schemas.StaffOut(
        id=s.id,
        name=s.name,
        age=s.age,
        department=s.department,
        basic_salary=s.basic_salary,
        bonus_percentage=s.bonus_percentage,
        bonus_amount=bonus_amount,
        final_salary=final_salary
    )

# Update Staff
@router.put("/staff/{staff_id}", response_model=schemas.StaffOut)
def update_staff(staff_id: int, staff_in: schemas.StaffUpdate, payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    s = db.query(Staff).filter(Staff.id == staff_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")

    for field, value in staff_in.model_dump(exclude_unset=True).items():
        setattr(s, field, value)
    db.commit()
    db.refresh(s)

    bonus_amount = getattr(staff_in, "bonus_amount", s.basic_salary * s.bonus_percentage / 100)
    bonus_percentage, final_salary = calculate_bonus_and_salary(s.basic_salary, bonus_amount)

    s.bonus_percentage = bonus_percentage
    db.commit()

    return schemas.StaffOut(
        id=s.id,
        name=s.name,
        age=s.age,
        department=s.department,
        basic_salary=s.basic_salary,
        bonus_percentage=bonus_percentage,
        bonus_amount=bonus_amount,
        final_salary=final_salary
    )

# Delete Staff
@router.delete("/staff/{staff_id}", status_code=204)
def delete_staff(staff_id: int, payload=Depends(auth.JWTBearer()), db: Session = Depends(get_db)):
    s = db.query(Staff).filter(Staff.id == staff_id).first()
    if not s:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Staff not found")
    db.delete(s)
    db.commit()
    return {"detail": "Staff deleted successfully"}
