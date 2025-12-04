# schemas.py
from pydantic import BaseModel, Field
from typing import Optional

# ------------------------------
# User Schemas
# ------------------------------

class UserCreate(BaseModel):
    username: str = Field(..., min_length=3)
    password: str = Field(..., min_length=6, max_length=72)  # bcrypt limit

class UserOut(BaseModel):
    id: int
    username: str
    is_active: bool

    model_config = {
        "from_attributes": True  # Pydantic v2 replacement for orm_mode
    }

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

# ------------------------------
# Staff (Employee) Schemas
# ------------------------------

class StaffBase(BaseModel):
    name: str
    age: int
    department: Optional[str] = None
    basic_salary: float
    bonus_amount: Optional[float] = 0.0  # input bonus amount

class StaffCreate(StaffBase):
    pass

class StaffUpdate(BaseModel):
    name: Optional[str] = None
    age: Optional[int] = None
    department: Optional[str] = None
    basic_salary: Optional[float] = None
    bonus_amount: Optional[float] = None

class StaffOut(BaseModel):
    id: int
    name: str
    age: int
    department: Optional[str]
    basic_salary: float
    bonus_percentage: float
    bonus_amount: float
    final_salary: float

    model_config = {
        "from_attributes": True
    }
