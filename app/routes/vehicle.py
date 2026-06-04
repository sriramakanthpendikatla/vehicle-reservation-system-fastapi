from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.db import get_db

from app.models.vehicle import Vehicle
from app.models.vehicle_status import Vehicle_status
from app.models.vehicle_logs import Vehicle_logs, Action

from app.schemas.vehicle import (
    CreateVehicle,
    VehicleResponse
)

router = APIRouter(
    prefix="/vehicles",
    tags=["Vehicles"]
)


# ==================================
# CREATE VEHICLE
# ==================================
@router.post("/", response_model=VehicleResponse)
def create_vehicle(vd: CreateVehicle,db: Session = Depends(get_db)):

    existing_vehicle = db.query(Vehicle).filter(Vehicle.number == vd.number).first()

    if existing_vehicle:
        raise HTTPException(status_code=400,detail="Vehicle number already exists")

    new_vehicle = Vehicle(
        type=vd.type,
        number=vd.number,
        department_id=vd.department_id,
        maintenance_intervel=vd.maintenance_intervel,
        maintenance_atkms=vd.maintenance_atkms,
        status=Vehicle_status.AVAILABLE
    )

    db.add(new_vehicle)
    db.flush()

    vehicle_log = Vehicle_logs(
        vehicle_id=new_vehicle.id,
        employee_id=None,
        department_id=new_vehicle.department_id,
        timestamp=datetime.utcnow(),
        action=Action.CREATED
    )

    db.add(vehicle_log)

    db.commit()
    db.refresh(new_vehicle)

    return new_vehicle


# ==================================
# GET ALL VEHICLES
# ==================================
@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(db: Session = Depends(get_db)):
    return db.query(Vehicle).all()


# ==================================
# GET VEHICLE BY ID
# ==================================
@router.get("/{vehicle_id}")
def get_vehicle(vehicle_id: int,db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404,detail="Vehicle not found")
    return vehicle


# ==================================
# GET VEHICLE STATUS
# ==================================
@router.get("/{vehicle_id}/status")
def get_vehicle_status(vehicle_id: int,db: Session = Depends(get_db)):

    vehicle = db.query(Vehicle).filter(Vehicle.id == vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=404,detail="Vehicle not found")

    return {
        "vehicle_id": vehicle.id,
        "vehicle_number": vehicle.number,
        "status": vehicle.status
    }


# ==================================
# GET VEHICLE LOGS
# ==================================
@router.get("/logs/all")
def get_vehicle_logs(db: Session = Depends(get_db)):
    return db.query(Vehicle_logs).all()