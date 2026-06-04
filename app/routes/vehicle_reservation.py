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

    try:

        with db.begin():

            # Check Department
            department = db.query(Department).filter(Department.id == cvr.department_id).first()

            if not department:
                raise HTTPException(status_code=404,detail="Department not found")

            # Check Employee
            employee = db.query(Employee).filter(Employee.id == cvr.employee_id).first()

            if not employee:
                raise HTTPException(status_code=404,detail="Employee not found")

            # Lock Vehicle Row (Concurrency Protection)
            vehicle = db.query(Vehicle).filter(Vehicle.id == cvr.vehicle_id).with_for_update().first()

            if not vehicle:
                raise HTTPException(status_code=404,detail="Vehicle not found")

            # Department Access Validation
            if employee.department_id != department.id:
                raise HTTPException(status_code=400,detail="Employee does not belong to selected department")
            
            # Check Vehicle Belongs to Department or not 
            if vehicle.department_id != department.id:
                raise HTTPException(status_code=400,detail="vehicle Dont Belongs to Department")

            # Driving License Validation
            if employee.driving_license_date < datetime.today():
                raise HTTPException(status_code=400,detail="Driving license expired")

            # Active Reservation Quota Validation
            active_reservations = db.query(Vechile_reservation).filter(
                Vechile_reservation.employee_id == employee.id,
                Vechile_reservation.reservation_end == None
            ).count()

            if active_reservations >= employee.vehicle_quota:
                raise HTTPException(status_code=400,detail="Employee vehicle quota exceeded")

            # Vehicle Availability Validation
            if vehicle.status != Vehicle_status.AVAILABLE:
                raise HTTPException(status_code=400,detail="Vehicle is not available")

            # Create Reservation
            reservation = Vechile_reservation(
                vehicle_id=cvr.vehicle_id,
                employee_id=cvr.employee_id,
                department_id=cvr.department_id
            )

            db.add(reservation)
            db.flush()

            # Update Vehicle Status
            vehicle.status = Vehicle_status.RESERVED

            # Create Audit Log
            vehicle_log = Vehicle_logs(
                vehicle_id=vehicle.id,
                employee_id=employee.id,
                department_id=department.id,
                timestamp=datetime.utcnow(),
                action=Action.RESERVED
            )

            db.add(vehicle_log)

        db.refresh(reservation)

        return reservation

    except HTTPException:
        raise

    except Exception as e:
        db.rollback()
        raise HTTPException(status_code=500,detail=f"Reservation failed: {str(e)}")


# ==================================
# GET ALL RESERVATIONS
# ==================================
@router.get("/", response_model=list[VehicleReservationResponse])
def get_reservations(db: Session = Depends(get_db)):
    return db.query(Vechile_reservation).all()


# ==================================
# GET RESERVATION BY ID
# ==================================
@router.get("/{reservation_id}", response_model=VehicleReservationResponse)
def get_reservation(reservation_id: int,db: Session = Depends(get_db)):

    reservation = db.query(Vechile_reservation).filter(Vechile_reservation.id == reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=404,detail="Reservation not found")

    return reservation


# ==================================
# GET VEHICLE LOGS
# ==================================
@router.get("/logs")
def get_logs(db: Session = Depends(get_db)):
    return db.query(Vehicle_logs).order_by(Vehicle_logs.timestamp.desc()).all()