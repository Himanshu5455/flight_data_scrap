from pydantic import BaseModel
from datetime import date
from typing import Optional
class FlightQuery(BaseModel):
    airline_code: str
    flight_number: str
    departure_date: date

class FlightResponse(BaseModel):
    id: Optional[int] = None  # Make this optional
    airline_code: str
    flight_number: str
    departure_date: date
    origin: str
    destination: str
    scheduled_departure_time: str
    actual_departure_time: str
    scheduled_arrival_time: str
    actual_arrival_time: str
    status: str
    duration: str
    codeshare_airline: str
    codeshare_flight_number: str
    aircraft_code: str
    aircraft_type: str

    class Config:
        orm_mode = True
