from sqlalchemy import Column, Integer, String, Date
from database import Base

class Flight(Base):
    __tablename__ = "flights"

    id = Column(Integer, primary_key=True, index=True)
    airline_code = Column(String)
    flight_number = Column(String)
    departure_date = Column(Date)
    origin = Column(String)
    destination = Column(String)
    scheduled_departure_time = Column(String)
    actual_departure_time = Column(String)
    scheduled_arrival_time = Column(String)
    actual_arrival_time = Column(String)
    status = Column(String)
    duration = Column(String)
    codeshare_airline = Column(String)
    codeshare_flight_number = Column(String)
    aircraft_code = Column(String)
    aircraft_type = Column(String)
