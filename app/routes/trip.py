from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from datetime import datetime

from app.utils.db import get_db

from app.models.trips import Trip
from app.models.vehicle import Vehicle, Vehicle_status
from app.models.vehicle_reservation import Vechile_reservation
from app.models.vehicle_logs import Vehicle_logs, Action
from app.models.maintenance_schedule import Maintenance_schedule

from app.schemas.trips import TripCheckout, TripCheckin

router = APIRouter(
    prefix="/trips",
    tags=["Trips"]
)


# ===========================
# TRIP CHECKOUT
# ===========================
@router.post("/")
def trip_checkout(ct: TripCheckout,db: Session = Depends(get_db)):

    reservation = db.query(Vechile_reservation).filter(Vechile_reservation.id == ct.reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=400,detail="Reservation not found")

    vehicle = db.query(Vehicle).filter(Vehicle.id == reservation.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=400,detail="Vehicle not found")

    if vehicle.status != Vehicle_status.RESERVED:
        raise HTTPException(status_code=400,detail="Vehicle is not reserved")

    existing_trip = db.query(Trip).filter(Trip.reservation_id == reservation.id,Trip.check_in_time == None).first()

    if existing_trip:
        raise HTTPException(status_code=400,detail="Trip already exists")

    new_trip = Trip(
        reservation_id=reservation.id,
        start_odometer=vehicle.current_odometer,
        end_odometer=None,
        fuel_level_before=ct.fuel_level_before,
        fuel_level_after=None,
        check_in_time=None,
        expected_end_time=ct.expected_end_time,
        actual_end_time=None
    )

    db.add(new_trip)

    vehicle.status = Vehicle_status.IN_USE

    vehicle_log = Vehicle_logs(
        department_id=reservation.department_id,
        employee_id=reservation.employee_id,
        vehicle_id=vehicle.id,
        timestamp=datetime.utcnow(),
        action=Action.CHECKED_OUT
    )

    db.add(vehicle_log)

    db.commit()
    db.refresh(new_trip)

    return new_trip


# ===========================
# TRIP CHECK-IN
# ===========================
@router.put("/")
def check_in(cti: TripCheckin,db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == cti.trip_id).first()

    if not trip:
        raise HTTPException(status_code=400,detail="Trip not found")

    reservation = db.query(Vechile_reservation).filter(Vechile_reservation.id == trip.reservation_id).first()

    if not reservation:
        raise HTTPException(status_code=400,detail="Reservation not found")

    vehicle = db.query(Vehicle).filter(Vehicle.id == reservation.vehicle_id).first()

    if not vehicle:
        raise HTTPException(status_code=400,detail="Vehicle not found")

    if trip.end_odometer is not None:
        raise HTTPException(status_code=400,detail="Trip already checked in")

    if trip.start_odometer is None:
        raise HTTPException(tatus_code=400,detail="Start odometer missing")

    if cti.end_odometer < trip.start_odometer:
        raise HTTPException(status_code=400,detail="Invalid odometer reading")

    if cti.fuel_level_after > trip.fuel_level_before:
        raise HTTPException(status_code=400,detail="Invalid fuel level")

    if vehicle.status != Vehicle_status.IN_USE:
        raise HTTPException(status_code=400,detail="Vehicle is not in use")

    trip.end_odometer = cti.end_odometer
    trip.fuel_level_after = cti.fuel_level_after
    trip.check_in_time = datetime.utcnow()
    trip.actual_end_time = datetime.utcnow()

    vehicle.current_odometer = cti.end_odometer

    checkin_log = Vehicle_logs(
        department_id=reservation.department_id,
        employee_id=reservation.employee_id,
        vehicle_id=vehicle.id,
        timestamp=datetime.utcnow(),
        action=Action.CHECKED_IN
    )

    reservation.reservation_end = datetime.utcnow()

    # Maintenance Check
    if vehicle.current_odometer >= vehicle.maintenance_atkms:

        vehicle.status = Vehicle_status.MAINTENANCE

        existing_maintenance = db.query(Maintenance_schedule).filter(
            Maintenance_schedule.vehicle_id == vehicle.id,
            Maintenance_schedule.maintenance_end == None
        ).first()

        if not existing_maintenance:

            maintenance = Maintenance_schedule(
                vehicle_id=vehicle.id,
                maintenance_start=datetime.utcnow(),
                maintenance_end=None,
                description="AUTO SCHEDULED MAINTENANCE"
            )

            db.add(maintenance)

            maintenance_log = Vehicle_logs(
                department_id=reservation.department_id,
                employee_id=reservation.employee_id,
                vehicle_id=vehicle.id,
                timestamp=datetime.utcnow(),
                action=Action.MAINTENANCE_STARTED
            )

            db.add(maintenance_log)

    else:
        vehicle.status = Vehicle_status.AVAILABLE

    

    db.add(checkin_log)

    db.commit()
    db.refresh(trip)

    return trip


# ===========================
# GET ALL TRIPS
# ===========================
@router.get("/")
def get_trips(db: Session = Depends(get_db)):
    return db.query(Trip).all()


# ===========================
# GET SINGLE TRIP
# ===========================
@router.get("/{trip_id}")
def get_trip(trip_id: int,db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404,detail="Trip not found")

    return trip


# ===========================
# OVERDUE TRIP
# ===========================
@router.put("/overdue/{trip_id}")
def overdue(trip_id: int,db: Session = Depends(get_db)):

    trip = db.query(Trip).filter(Trip.id == trip_id).first()

    if not trip:
        raise HTTPException(status_code=404,detail="Trip not found")

    if trip.expected_end_time >= datetime.utcnow():
        raise HTTPException(status_code=400,detail="Trip is not overdue")

    reservation = db.query(Vechile_reservation).filter(Vechile_reservation.id == trip.reservation_id).first()

    vehicle_log = Vehicle_logs(
        department_id=reservation.department_id,
        employee_id=reservation.employee_id,
        vehicle_id=reservation.vehicle_id,
        timestamp=datetime.utcnow(),
        action=Action.OVERDUE
    )

    db.add(vehicle_log)
    db.commit()

    return {
        "message": "Trip marked as overdue"
    }