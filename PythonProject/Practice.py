from fastapi import FastAPI
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base

engine= create_engine("sqlite:///mechanics.db")

Base= declarative_base()

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
class MechanicDB(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    service = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

app = FastAPI()

class Mechanic(BaseModel):
 id:int
name: str
service:str
lat: float
lng: float
phone: str

mechanics= [
    {"id":1,"name": "John Doe", "services": "Engine Repair", "lat":37.4421,"lng": 122.3342, "phone": 123-456-789,},
    {"id":2, "name": "Kwame Bonsu", "services": "Brake Repair/Replacement", "lat": 24.4366,"lng": 145.3456, "phone": 213-546-987},
    {"id":3, "name": "Mike Wale", "services": "Car Air-conditioning", "lat":43.2234,"lng": 113.5643, "phone": 113-564-987},
]
@app.get("/")
def home():
    return {"message": "Welcome to the Mechanincs API"}

@app.get("/mechanics")
def get_mechanics():
    return  mechanics

@app.get("/mechanics/{mechanic_id}")
def get_mechanic(mechanic_id: int):
    mechanic = next((m for m in mechanics if m["id"] == mechanic_id), None)
    if mechanic:
        return mechanic
    return {"message": "Mechanic not found"}

@app.post("/mechanics")
def add_mechanic(mechanic: Mechanic):
    mechanics.append(mechanic)
    return {"message": "Mechanic added succesfully","mechanic":mechanic}

@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic(mechanic_id: int):
    for mechanic in mechanics:
        if mechanic["id"] == mechanic_id:
            mechanics.remove(mechanic)
            return{"message": "Mechanic deleted Successfully"}
    return{"error": "Mechanic not found"}

@app.put("/mechanics/{mechanic_id}")
def update_mechanic(mechanic_id: int, updated_mechanic: Mechanic):
    for i, mechanic in enumerate(mechanics):
        if mechanic["id"] == mechanic_id:
            mechanics[i] = updated_mechanic.model_dump()
            return {
                "message": "Mechanic updated successfully",
                "mechanic": updated_mechanic
            }
    return {"error": "Mechanic not found"}