from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy import create_engine, Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker, declarative_base, Session

"""
DATABASE CONNECTION
"""

DATABASE_URL = "sqlite:///mechanics.db"
engine = create_engine(
    DATABASE_URL,
    connect_args={"check_same_thread": False}
)
SessionLocal = sessionmaker(
    autocommit=False, 
    autoflush=False, 
    bind=engine
)

Base = declarative_base()

"""
DATABASE TABLE
"""

class MechanicDB(Base):
    __tablename__ = "mechanics"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String)
    service = Column(String)
    lat = Column(Float)
    lng = Column(Float)
    phone = Column(String)

Base.metadata.create_all(bind=engine)

""""
DATABASE SEESION
""""

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
""""
PYDANTIC MODELS
""""

class MechanicCreate(BaseModel):
    id: int
    name: str
    service: str
    lat: float
    lng: float
    phone: str

class MechanicUpdate(BaseModel):
    id: int
    name: str
    service: str
    lat: float
    lng: float
    phone: str

class MechanicResponse(BaseModel):
    id: int
    name: str
    service: str
    lat: float
    lng: float
    phone: str

    model_config = {
        "from_attributes": True
    }
""""
FASTAPI APPLICATION
""""
app = FastAPI()

@app.get("/")
def home():
    return {"message": "Welcome to the Mechanics API"}

""""
GET ALL MECHANICS
""""
@app.get("/mechanics")
def get_mechanics(db: Session = Depends(get_db)):
    return db.query(MechanicDB).all()
"""""
GET ONE MECHANIC
"""""

@app.get("/mechanics/{mechanic_id}")
def get_mechanic(
    mechanic_id: int, 
    db: Session = Depends(get_db)
):
    mechanic = (
        db.query(MechanicDB)
        .filter(MechanicDB.id == mechanic_id)
        .first()
    )   
    if mechanic is None:
        raise HTTPException(
            status_code=404, 
            detail="Mechanic not found"
        )
    return mechanic

""""
ADD A MECHANIC
""""

@app.post(
    "/mechanics",
    response_model=MechanicResponse,
    status_code+status.HTTP_201_CREATED
)
def add_mechanic(
    mechanic: Mechanic, 
    db: Session = Depends(get_db)
):
    db_mechanic = MechanicDB(**mechanic.model_dump())
    db.add(db_mechanic)
    db.commit()
    db.refresh(db_mechanic)
    
    return db_mechanic

""""
DELETE A MECHANIC
""""
@app.delete("/mechanics/{mechanic_id}")
def delete_mechanic(
    mechanic_id: int,
    db: Session = Depends(get_db)
):
    mechanic = (db.query(MechanicDB)
    .filter(MechanicDB.id == mechanic_id)
    .first()
    )
    if mechanic is None:
        raise HTTPException(
            status_code=404, 
            detail="Mechanic not found"
        )
    db.delete(mechanic)
    db.commit()
    
    return {"message": "Mechanic deleted successfully"}

""""
UPDATE A MECHANIC
""""

@app.put("/mechanics/{mechanic_id}",
        response_model=MechanicResponse
)

def update_mechanic(
    mechanic_id: int, 
    updated_mechanic: Mechanic,
    db: Session = Depends(get_db)
):
    mechanic = (
        db.query(MechanicDB)
        .filter(MechanicDB.id == mechanic_id)
        .first()
    )
    if mechanic is None:
        raise HTTPException(
            status_code=404, 
            detail="Mechanic not found"
        )
    for key, value in updated_mechanic.model_dump().items():
        setattr(mechanic, key, value)
    db.commit()
    db.refresh(mechanic)
    return mechanic
