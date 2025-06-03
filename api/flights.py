from fastapi import APIRouter, Query, HTTPException, Depends
from sqlalchemy.orm import Session
from database import SessionLocal
from models import Flight
from schemas import FlightResponse
from scraper import scrape_flight_data
from datetime import datetime, date

router = APIRouter(prefix="/track-flight", tags=["Flights"])

# Dependency to get DB session
def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.get('/')
def home():
    return "hello welcome to flight scraping"

@router.get("/flight", response_model=FlightResponse)
def track_flight(
    airline_code: str = Query(...),
    flight_number: str = Query(...),
    departure_date: str = Query(...),
    db: Session = Depends(get_db)
):
    # Parse departure_date to a date object
    try:
        departure_date_obj = datetime.strptime(departure_date, "%Y-%m-%d").date()
    except ValueError:
        raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD.")

    # Check if flight exists in the database
    existing = db.query(Flight).filter_by(
        airline_code=airline_code,
        flight_number=flight_number,
        departure_date=departure_date_obj
    ).first()
    if existing:
        return existing

    # Scrape flight data
    scraped_data = scrape_flight_data(airline_code, flight_number, departure_date)
    if not scraped_data:
        raise HTTPException(status_code=404, detail="Flight data not found")

    # Ensure departure_date in scraped_data is a date object
    if isinstance(scraped_data.get('departure_date'), str):
        try:
            scraped_data['departure_date'] = datetime.strptime(scraped_data['departure_date'], "%Y-%m-%d").date()
        except ValueError:
            raise HTTPException(status_code=400, detail="Invalid departure_date format in scraped data. Use YYYY-MM-DD.")
    print(scraped_data)
    # Create and save flight to database
    flight = Flight(**scraped_data)
    db.add(flight)
    db.commit()
    db.refresh(flight)
    return scraped_data