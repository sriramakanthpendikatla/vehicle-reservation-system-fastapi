from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.db import get_db

from app.models.department import Department
from app.models.employee import Employee
from app.models.vehicle import Vehicle, Vehicle_status
from app.models.vehicle_reservation import Vechile_reservation
from app.models.vehicle_logs import Vehicle_logs, Action

from app.schemas.vehicle_reservation import (
    CreateVehicleReservation,
    VehicleReservationResponse
)

router = APIRouter(
    prefix="/vehicle_reservations",
    tags=["Vehicle Reservations"]
)


# ==================================
# CREATE RESERVATION
# ==================================
@router.post("/", response_model=VehicleReservationResponse)
def create_vehicle_reservation(cvr: CreateVehicleReservation,db: Session = Depends(get_db)):

    # Check Department
    department = db.query(Department).filter(Department.id == cvr.department_id).first()

    if not department:
        raise HTTPException(status_code=404,detail="Department not found")

    # Check Employee
    employee = db.query(Employee).filter(Employee.id == cvr.employee_id).first()

    if not employee:
        raise HTTPException(status_code=404,detail="Employee not found")

    # Check Vehicle
    vehicle = db.query(Vehicle).filter(Vehicle.id == cvr.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404,detail="Vehicle not found"
        )

    # Employee belongs to department
    if employee.department_id != department.id:
        raise HTTPException(status_code=400,detail="Employee does not belong to selected department")

    # Driving License Validation
    if employee.driving_license_date < datetime.utcnow():
        raise HTTPException(status_code=400,detail="Driving license expired")

    # Employee quota check
    active_reservations = db.query(Vechile_reservation).filter(
        Vechile_reservation.employee_id == employee.id,
        Vechile_reservation.reservation_end == None).count()

    if active_reservations >= employee.vehicle_quota:
        raise HTTPException(status_code=400,detail="Employee vehicle quota exceeded")

    # Vehicle availability check
    if vehicle.status != Vehicle_status.AVAILABLE:
        raise HTTPException(status_code=400,detail="Vehicle is not available")

    # Create reservation
    reservation = Vechile_reservation(
        vehicle_id=cvr.vehicle_id,
        employee_id=cvr.employee_id,
        department_id=cvr.department_id
    )

    db.add(reservation)
    db.flush()

    # Update vehicle status
    vehicle.status = Vehicle_status.RESERVED

    # Create log
    vehicle_log = Vehicle_logs(
        vehicle_id=vehicle.id,
        employee_id=employee.id,
        department_id=department.id,
        timestamp=datetime.utcnow(),
        action=Action.RESERVED
    )

    db.add(vehicle_log)

    db.commit()
    db.refresh(reservation)

    return reservation


# ==================================
# GET ALL RESERVATIONS
# ==================================
@router.get("/", response_model=list[VehicleReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Vechile_reservation).all()


# ==================================
# GET ALL LOGS
# ==================================
@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(Vehicle_logs).all()