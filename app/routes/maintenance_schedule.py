from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.db import get_db

from app.models.maintenance_schedule import Maintenance_schedule
from app.models.vehicle import Vehicle, Vehicle_status
from app.models.vehicle_logs import Vehicle_logs, Action

from app.schemas.maintenance_schedule import (
    CreateMaintenanceSchedule,
    MaintenanceScheduleResponse
)

router = APIRouter(
    prefix="/maintenance_schedules",
    tags=["Maintenance Schedules"]
)


# ==================================
# CREATE MAINTENANCE SCHEDULE
# ==================================
@router.post("/", response_model=MaintenanceScheduleResponse)
def create_maintenance_schedule(schedule: CreateMaintenanceSchedule,db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(Vehicle.id == schedule.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404,detail="Vehicle not found")

    existing_maintenance = db.query(Maintenance_schedule).filter(
        Maintenance_schedule.vehicle_id == vehicle.id,
        Maintenance_schedule.maintenance_end == None).first()

    if existing_maintenance:
        raise HTTPException(status_code=400,detail="Maintenance already scheduled for this vehicle")

    maintenance = Maintenance_schedule(
        vehicle_id=schedule.vehicle_id,
        maintenance_start=schedule.maintenance_start,
        maintenance_end=None,
        description=schedule.description
    )

    vehicle.status = Vehicle_status.MAINTENANCE

    maintenance_log = Vehicle_logs(
        department_id=vehicle.department_id,
        employee_id=None,
        vehicle_id=vehicle.id,
        timestamp=datetime.utcnow(),
        action=Action.MAINTENANCE_STARTED
    )

    db.add(maintenance)
    db.add(maintenance_log)

    db.commit()
    db.refresh(maintenance)

    return maintenance


# ==================================
# COMPLETE MAINTENANCE
# ==================================
@router.put("/{MID}/complete")
def complete_maintenance(MID: int,db: Session = Depends(get_db)):

    maintenance = db.query(Maintenance_schedule).filter(Maintenance_schedule.id == MID).first()

    if not maintenance:
        raise HTTPException(status_code=404,detail="Maintenance schedule not found"
        )

    if maintenance.maintenance_end is not None:
        raise HTTPException(status_code=400,detail="Maintenance already completed")

    vehicle = db.query(Vehicle).filter(Vehicle.id == maintenance.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404,detail="Vehicle not found")

    maintenance.maintenance_end = datetime.utcnow()

    vehicle.status = Vehicle_status.AVAILABLE

    vehicle.maintenance_atkms += vehicle.maintenance_intervel

    maintenance_log = Vehicle_logs(
        department_id=vehicle.department_id,
        employee_id=None,
        vehicle_id=vehicle.id,
        timestamp=datetime.utcnow(),
        action=Action.MAINTENANCE_COMPLETED
    )

    db.add(maintenance_log)

    db.commit()
    db.refresh(maintenance)

    return {
        "message": "Maintenance completed successfully",
        "maintenance": maintenance
    }


# ==================================
# GET ALL MAINTENANCE SCHEDULES
# ==================================
@router.get("/")
def get_maintenance_schedules(db: Session = Depends(get_db)):
    return db.query(Maintenance_schedule).all()


# ==================================
# GET SINGLE MAINTENANCE SCHEDULE
# ==================================
@router.get("/{MID}")
def get_maintenance_schedule(MID: int,db: Session = Depends(get_db)):

    maintenance = db.query(Maintenance_schedule).filter(Maintenance_schedule.id == MID).first()
    if not maintenance:
        raise HTTPException(status_code=404,detail="Maintenance schedule not found")
    return maintenance