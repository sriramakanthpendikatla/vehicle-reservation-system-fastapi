from app.database import Base , engine ,SessionLocal

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()