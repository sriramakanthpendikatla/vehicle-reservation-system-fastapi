from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.models.department import Department
from app.schemas.department import DepartmentCreate,DepartmentResponse

from app.utils.db import get_db

router = APIRouter(
    prefix="/departments",
    tags=["Departments"]
)


# ==========================
# CREATE DEPARTMENT
# ==========================
@router.post("/", response_model=DepartmentResponse)
def create_department(department: DepartmentCreate,db: Session = Depends(get_db)):

    existing_department = db.query(Department).filter(Department.title == department.title).first()

    if existing_department:
        raise HTTPException(status_code=400,detail="Department already exists")

    new_department = Department(
        title=department.title
    )

    db.add(new_department)
    db.commit()
    db.refresh(new_department)

    return new_department


# ==========================
# GET ALL DEPARTMENTS
# ==========================
@router.get("/", response_model=list[DepartmentResponse])
def get_departments(db: Session = Depends(get_db)):
    return db.query(Department).all()


# ==========================
# GET DEPARTMENT BY ID
# ==========================
@router.get("/{department_id}", response_model=DepartmentResponse)
def get_department(department_id: int,db: Session = Depends(get_db)):

    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")

    return department


# ==========================
# UPDATE DEPARTMENT
# ==========================
@router.put("/{department_id}", response_model=DepartmentResponse)
def update_department(department_id: int,department_data: DepartmentCreate,db: Session = Depends(get_db)):

    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")

    duplicate = db.query(Department).filter(
        Department.title == department_data.title,
        Department.id != department_id
    ).first()

    if duplicate:
        raise HTTPException(status_code=400,detail="Department title already exists")

    department.title = department_data.title

    db.commit()
    db.refresh(department)

    return department


# ==========================
# DELETE DEPARTMENT
# ==========================
@router.delete("/{department_id}")
def delete_department(department_id: int,db: Session = Depends(get_db)):

    department = db.query(Department).filter(Department.id == department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")

    db.delete(department)
    db.commit()

    return {
        "message": "Department deleted successfully"
    }