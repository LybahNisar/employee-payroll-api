# database.py
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
import psycopg
import os
from dotenv import load_dotenv

# Load .env file
load_dotenv()  # automatically loads variables from .env

# Fetch DB credentials from environment variables
DB_USER = os.getenv("DB_USER")
DB_PASS = os.getenv("DB_PASS")
DB_HOST = os.getenv("DB_HOST")
DB_PORT = os.getenv("DB_PORT")
DB_NAME = os.getenv("DB_NAME")

# Secret check
if not all([DB_USER, DB_PASS, DB_HOST, DB_PORT, DB_NAME]):
    raise EnvironmentError("Database credentials are missing in .env file!")

# Construct the PostgreSQL URL
POSTGRES_URL = f"postgresql+psycopg://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# Function to create database if it doesn't exist
def create_database():
    try:
        with psycopg.connect(
            f"host={DB_HOST} user={DB_USER} password={DB_PASS} dbname=postgres", autocommit=True
        ) as conn:
            with conn.cursor() as cur:
                cur.execute(f"CREATE DATABASE {DB_NAME}")
                print(f"Database '{DB_NAME}' created successfully!")
    except psycopg.errors.DuplicateDatabase:
        print(f"Database '{DB_NAME}' already exists, skipping creation.")
    except Exception as e:
        print("Error creating database:", e)

# Call only for development (comment out in production)
create_database()

# SQLAlchemy setup
engine = create_engine(POSTGRES_URL, echo=False)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
