"""
Run this once to load sample mechanics into mechanics.db:

    python seed_data.py
"""
from main import SessionLocal, MechanicDB

sample_mechanics = [
    {"name": "John Doe", "service": "Engine Repair", "lat": 37.4421, "lng": 122.3342, "phone": "123-456-789"},
    {"name": "Kwame Bonsu", "service": "Brake Repair/Replacement", "lat": 24.4366, "lng": 145.3456, "phone": "213-546-987"},
    {"name": "Mike Wale", "service": "Car Air-conditioning", "lat": 43.2234, "lng": 113.5643, "phone": "113-564-987"},
]

db = SessionLocal()
try:
    for m in sample_mechanics:
        db.add(MechanicDB(**m))
    db.commit()
    print(f"Seeded {len(sample_mechanics)} mechanics.")
finally:
    db.close()
