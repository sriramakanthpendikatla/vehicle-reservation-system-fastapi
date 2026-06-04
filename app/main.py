from fastapi import FastAPI
from app.models import department, employee,vehicle,vehicle_logs,vehicle_reservation,vehicle_status,maintenance_schedule,trips
from app.schemas import*
from app.database import Base , engine
from app.utils.db import get_db
from app.routes.department import router as dept_router
from app.routes.employee import router as emp_router
from app.routes.vehicle import router as ve_router
from app.routes.vehicle_reservation import router as vr_router
from app.routes.trip import router as trip_router
from app.routes.maintenance_schedule import router as ms_router

app =FastAPI()

Base.metadata.create_all(bind=engine)

app.include_router(dept_router)
app.include_router(emp_router)
app.include_router(ve_router)
app.include_router(vr_router)
app.include_router(trip_router)
app.include_router(ms_router)

@app.get("/")
def home():
    return {
        "message" : "Running"
    }