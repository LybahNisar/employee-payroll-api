# main.py
from fastapi import FastAPI
from database import engine, Base
import models
from routers import routes  # import combined router

# Create tables (only for development; Alembic should be used in production)
Base.metadata.create_all(bind=engine)

app = FastAPI(title="Employee Payroll & Staff API")

# Include the combined router (auth + staff CRUD)
app.include_router(routes.router)

# Root endpoint
@app.get("/")
def root():
    return {"message": "Employee Payroll & Staff API is running"}
