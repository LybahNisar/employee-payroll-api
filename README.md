# Employee Payroll & Staff Management API

A **FastAPI-based backend application** for managing employees, their payroll, and bonus calculations. This API allows user authentication, CRUD operations for staff data, and automatic salary calculations, including bonus and final salary.  

---

## 🔹 Features

- **User Authentication**:  
  - User signup and login with hashed passwords  
  - JWT-based token authentication for secure routes  

- **Staff Management (CRUD)**:  
  - Add new staff with basic salary and bonus  
  - Update staff details including salary adjustments  
  - Delete staff records  
  - Retrieve single or all staff details  

- **Payroll Calculation**:  
  - Calculates `bonus_percentage` automatically if salary and bonus amount are given  
  - Computes `final_salary` as:  
    ```text
    final_salary = basic_salary + (basic_salary * bonus_percentage / 100)
    ```  
  - Returns `bonus_amount` for transparency  

- **Database Migrations with Alembic**:  
  - Use Alembic to handle database schema changes without losing data  
  - Keeps development and production databases consistent  

- **Secure & Clean**:  
  - Uses `.env` file to hide sensitive database credentials  
  - Proper HTTP status codes and error handling  
  - Follows FastAPI best practices  

---

## 🔹 Technologies Used

- **Backend**: FastAPI, Python 3.12+  
- **Database**: PostgreSQL  
- **ORM**: SQLAlchemy  
- **Migrations**: Alembic  
- **Authentication**: JWT (JSON Web Tokens)  
- **Environment Variables**: python-dotenv  

---

## 🔹 Project Structure

