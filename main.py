from fastapi import FastAPI
from database import Base, engine
from api import flights

app = FastAPI(title="Flight Tracker API")
Base.metadata.create_all(bind=engine)
app.include_router(flights.router)
