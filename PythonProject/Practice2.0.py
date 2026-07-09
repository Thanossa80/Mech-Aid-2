from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session

engine = create_engine("sqlite:///mechanics.db")

Base = declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


class MechanicDB(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    service = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String)


Base.metadata.create_all(bind=engine)


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


app = FastAPI()


class Mechanic(BaseModel):
    id: int
    name: str
    service: str
    lat: float
    lng: float
    phone: str


INITIAL_MECHANICS = [
    {"id": 1, "name": "John Doe", "service": "Engine Repair", "lat": 37.4421, "lng": 122.3342, "phone": "123-456-789"},
    {"id": 2, "name": "Kwame Bonsu", "service": "Brake Repair/Replacement", "lat": 24.4366, "lng": 145.3456, "phone": "213-546-987"},
    {"id": 3, "name": "Mike Wale", "service": "Car Air-conditioning", "lat": 43.2234, "lng": 113.5643, "phone": "113-564-987"},
]


@app.on_event("startup")
def seed_database():
    db = SessionLocal()
    try:
        if db.query(MechanicDB).count() == 0:
            db.bulk_insert_mappings(MechanicDB, INITIAL_MECHANICS)
            db.commit()
    finally:
        db.close()


@app.get("/")
def home():
    return {"message": "Welcome to the Mechanics API"}


@app.get("/mechanics")
def get_mechanics(db: Session = Depends(get_db)):
    return db.query(MechanicDB).all()


@app.get("/mechanics/{mechanic_id}")
def get_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(MechanicDB).filter(MechanicDB.id == mechanic_id).first()
    if mechanic:
        return mechanic
    raise HTTPException(status_code=404, detail="Mechanic not found")


@app.post("/mechanics")
def add_mechanic(mechanic: Mechanic, db: Session = Depends(get_db)):
    db_mechanic = MechanicDB(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    return {"message": "Mechanic added successfully", "mechanic": db_mechanic}


@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic(mechanic_id: int, db: Session = Depends(get_db)):
    mechanic = db.query(MechanicDB).filter(MechanicDB.id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    db.delete(mechanic)
    db.commit()
    return {"message": "Mechanic deleted successfully"}


@app.put("/mechanics/{mechanic_id}")
def update_mechanic(mechanic_id: int, updated_mechanic: Mechanic, db: Session = Depends(get_db)):
    mechanic = db.query(MechanicDB).filter(MechanicDB.id == mechanic_id).first()
    if not mechanic:
        raise HTTPException(status_code=404, detail="Mechanic not found")
    for key, value in updated_mechanic.model_dump().items():
        setattr(mechanic, key, value)
    db.commit()
    db.refresh(mechanic)
    return {"message": "Mechanic updated successfully", "mechanic": mechanic}
