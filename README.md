# Flight Data Scraper

A Python-based flight data scraping application that extracts flight information from Flightstats using Selenium and BeautifulSoup. The project includes a FastAPI web service to provide flight data through RESTful API endpoints.

## Features

- 🛫 Scrape real-time flight data from Flightstats
- 📊 Extract comprehensive flight details (airports, times, status, aircraft info)
- 🚀 FastAPI web service with interactive Swagger documentation
- 💾 SQLite database integration for data persistence
- 🔄 Auto-reload development server
- 📝 Structured data validation with Pydantic schemas

## Project Structure

```
flight-data-scraper/
├──api  # Folder
└──flights.py           # Main api code 
├── scraper.py          # Core scraping functionality
├── main.py             # FastAPI application
├── database.py         # Database operations
├── models.py           # SQLAlchemy models
├── schemas.py          # Pydantic schemas
├── flights.db          # SQLite database
├── requirements.txt    # Python dependencies
└── README.md          # Project documentation

```

## Prerequisites

- Python 3.9 or higher
- Google Chrome browser
- ChromeDriver (matching your Chrome version)

## Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Himanshu5455/flight_data_scrap.git
   cd flight-data-scraper
   ```

2. **Create a virtual environment** (recommended)
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Setup ChromeDriver**
   - Download ChromeDriver from [chromedriver.chromium.org](https://chromedriver.chromium.org/)
   - Ensure the version matches your Chrome browser
   - Add ChromeDriver to your system PATH, or place it in the project directory

## Usage

### Starting the API Server

1. **Run the FastAPI application**
   ```bash
   uvicorn main:app --reload
   ```

2. **Access the API documentation**
   Open your browser and navigate to:
   ```
   http://127.0.0.1:8000/docs
   ```

### API Endpoints

#### Scrape Flight Data
- **Endpoint**: `POST /flight`
- **Description**: Scrape flight data for a specific flight
- **Request Body**:
  ```json
  {
    "airline_code": "MH",
    "flight_number": "716",
    "departure_date": "2025-06-03"
  }
  ```

#### Example Usage

**Using curl**:
```bash
curl -X POST "http://127.0.0.1:8000/flight" \
  -H "Content-Type: application/json" \
  -d '{
    "airline_code": "MH",
    "flight_number": "716",
    "departure_date": "2025-06-03"
  }'
```

## Response Format

The API returns flight data in the following format:

```json
{
  "id": null,
  "airline_code": "MH",
  "flight_number": "716",
  "departure_date": "2025-06-03",
  "origin": "CGK (CGK)",
  "destination": "Jakarta (KUL)",
  "scheduled_departure_time": "12:15 WIB",
  "actual_departure_time": "13:15 WIB",
  "scheduled_arrival_time": "15:25 +08",
  "actual_arrival_time": "16:27 +08",
  "status": "Arrived, Delayed by 1h 2m",
  "duration": "2h 12m",
  "codeshare_airline": "Firefly",
  "codeshare_flight_number": "7384",
  "aircraft_code": "73H",
  "aircraft_type": "Boeing 737"
}
```

## Dependencies

- **fastapi**: Modern web framework for building APIs
- **uvicorn**: ASGI server for FastAPI
- **selenium**: Web browser automation
- **beautifulsoup4**: HTML parsing
- **sqlalchemy**: SQL toolkit and ORM
- **pydantic**: Data validation using Python type annotations

## Development

### Running in Development Mode

The `--reload` flag enables automatic reloading when code changes are detected:

```bash
uvicorn main:app --reload --host 0.0.0.0 --port 8000
```

**Note**: Make sure to comply with website terms of service and implement appropriate delays between requests when scraping data.
