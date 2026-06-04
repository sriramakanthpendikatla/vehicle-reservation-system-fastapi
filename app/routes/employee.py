from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.employee import Employee
from app.models.department import Department
from app.schemas.employee import (
    CreateEmployee,
    EmployeeUpdate,
    EmployeeResponse
)
from app.utils.db import get_db
from datetime import date

router = APIRouter(
    prefix="/employees",
    tags=["Employees"]
)


# ==========================
# CREATE EMPLOYEE
# ==========================
@router.post("/", response_model=EmployeeResponse)
def create_employee(employee: CreateEmployee,db: Session = Depends(get_db)):

    existing_employee = db.query(Employee).filter(Employee.addharcard == employee.addharcard).first()

    if existing_employee:
        raise HTTPException(status_code=400,detail="Employee already exists")

    department = db.query(Department).filter(Department.id == employee.department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")
    
    if employee.driving_license_date <= date.today():
        raise HTTPException(status_code=400,detail="Driving license already expired")

    new_employee = Employee(
        name=employee.name,
        addharcard=employee.addharcard,
        department_id=employee.department_id,
        driving_license_date=employee.driving_license_date,
        vehicle_quota=employee.vehicle_quota
    )

    db.add(new_employee)
    db.commit()
    db.refresh(new_employee)

    return new_employee


# ==========================
# GET ALL EMPLOYEES
# ==========================
@router.get("/", response_model=list[EmployeeResponse])
def get_employees(db: Session = Depends(get_db)):
    return db.query(Employee).all()


# ==========================
# GET EMPLOYEE BY ID
# ==========================
@router.get("/{employee_id}", response_model=EmployeeResponse)
def get_employee(employee_id: int,db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee not found")

    return employee


# ==========================
# UPDATE EMPLOYEE
# ==========================
@router.put("/{employee_id}", response_model=EmployeeResponse)
def update_employee(employee_id: int,employee_data: EmployeeUpdate,db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee not found")

    department = db.query(Department).filter(Department.id == employee_data.department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found"
        )

    employee.name = employee_data.name
    employee.addharcard = employee_data.addharcard
    employee.department_id = employee_data.department_id
    employee.driving_license_date = employee_data.driving_license_date
    employee.vehicle_quota = employee_data.vehicle_quota

    db.commit()
    db.refresh(employee)

    return employee


# ==========================
# DELETE EMPLOYEE
# ==========================
@router.delete("/{employee_id}")
def delete_employee(employee_id: int,db: Session = Depends(get_db)):

    employee = db.query(Employee).filter(Employee.id == employee_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee not found"
        )

    db.delete(employee)
    db.commit()

    return {
        "message": "Employee deleted successfully"
    }