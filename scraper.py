
import re
from datetime import date
from bs4 import BeautifulSoup
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.chrome.options import Options

def scrape_flight_data(airline_code: str, flight_number: str, departure_date: date):
    """
    Scrape flight data from Flightstats using Selenium and JSON parsing.
    Args:
        airline_code: e.g., 'MH' for Malaysia Airlines
        flight_number: e.g., '716'
        departure_date: date object for the flight date
    Returns:
        Dictionary with flight details or None if scraping fails
    """
    try:
        # Set up Selenium with headless Chrome
        options = Options()
        options.add_argument('--headless')
        options.add_argument('--disable-gpu')
        options.add_argument('user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36')
        driver = webdriver.Chrome(options=options)
        
        # Construct the URL
        url = f"https://www.flightstats.com/v2/flight-tracker/{airline_code}/{flight_number}?date={departure_date}"
        print(f"Accessing URL: {url}")
        driver.get(url)
        
        # Wait for page to load
        try:
            WebDriverWait(driver, 15).until(
                EC.presence_of_element_located((By.XPATH, "//*[contains(text(), 'Flight Status') or contains(text(), 'Arrived')]"))
            )
        except Exception as e:
            print(f"Error: Flight details not found. Possible CAPTCHA or page structure issue: {e}")
            with open("page_source.html", "w", encoding="utf-8") as f:
                f.write(driver.page_source)
            print("Saved page source to 'page_source.html' for inspection.")
            driver.quit()
            return None
        
        # Parse page source
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        
        # # Debug: Save page source
        # with open("page_source.html", "w", encoding="utf-8") as f:
        #     f.write(driver.page_source)

        flight_info = {
            'airline_code': airline_code,
            'flight_number': flight_number,
            'departure_date': str(departure_date),
            'origin': '',
            'destination': '',
            'scheduled_departure_time': '',
            'actual_departure_time': '',
            'scheduled_arrival_time': '',
            'actual_arrival_time': '',
            'status': '',
            'duration': '',
            'codeshare_airline': '',
            'codeshare_flight_number': '',
            'aircraft_code': '',
            'aircraft_type': ''
        }
        
        # Extract Origin and Destination
        flight_status_section = soup.find("div", string=re.compile("Flight Status", re.IGNORECASE))
        if flight_status_section:
            parent = flight_status_section.find_parent()
            if parent:
                # Find airport codes (3-letter codes like CGK, KUL)
                airport_elements = parent.find_all("div", string=re.compile(r"^[A-Z]{3}$"))
                # Find city names (exclude airline names and other keywords)
                city_elements = parent.find_all("div", string=re.compile(r"^[A-Za-z\s]+$", re.IGNORECASE))
                city_elements = [c for c in city_elements if c.text.strip() not in [airline_code, flight_number, 'Flight Status', 'Malaysia Airlines', 'Firefly'] and len(c.text.strip().split()) <= 3]
                
                if len(airport_elements) >= 2 and len(city_elements) >= 2:
                    flight_info['origin'] = f"{city_elements[0].text.strip()} ({airport_elements[0].text.strip()})"
                    flight_info['destination'] = f"{city_elements[1].text.strip()} ({airport_elements[1].text.strip()})"
        
        # Text-based extraction for other fields
        divs = soup.find_all("div")
        for div in divs:
            text = div.text.strip()
            text_lower = text.lower()
            
            # Status
            if "arrived" in text_lower and "delayed by" in text_lower:
                match = re.search(r"Arrived\s*Delayed by\s*([\w\s]+)", text, re.IGNORECASE)
                if match:
                    flight_info['status'] = f"Arrived, Delayed by {match.group(1).strip()}"
            
            # Times
            if "scheduled" in text_lower and "wib" in text_lower:
                match = re.search(r"Scheduled\s*(\d{2}:\d{2}\s*WIB)", text)
                if match:
                    flight_info['scheduled_departure_time'] = match.group(1)
            if "actual" in text_lower and "wib" in text_lower:
                match = re.search(r"Actual\s*(\d{2}:\d{2}\s*WIB)", text)
                if match:
                    flight_info['actual_departure_time'] = match.group(1)
            if "scheduled" in text_lower and "+08" in text_lower:
                match = re.search(r"Scheduled\s*(\d{2}:\d{2}\s*\+08)", text)
                if match:
                    flight_info['scheduled_arrival_time'] = match.group(1)
            if "actual" in text_lower and "+08" in text_lower:
                match = re.search(r"Actual\s*(\d{2}:\d{2}\s*\+08)", text)
                if match:
                    flight_info['actual_arrival_time'] = match.group(1)
            
            # Duration
            if "flight time" in text_lower and "total" in text_lower:
                match = re.search(r"Total\s*(\d+h\s*\d+m)", text)
                if match:
                    flight_info['duration'] = match.group(1)
            
            # Codeshare and Aircraft
            if "codeshare airline" in text_lower:
                match = re.search(r"Codeshare Airline\s*([\w\s]+)\s*Flight Number\s*\((\w+)\)\s*(\d+)", text, re.IGNORECASE)
                if match:
                    flight_info['codeshare_airline'] = match.group(1).strip()
                    flight_info['codeshare_flight_number'] = match.group(3).strip()
            if "aircraft equipment" in text_lower:
                if "code" in text_lower:
                    match = re.search(r"Code\s*(\w{3})", text)
                    if match:
                        flight_info['aircraft_code'] = match.group(1)
                if "description" in text_lower:
                    match = re.search(r"Description\s*(Boeing [\w\s()/]+)", text, re.IGNORECASE)
                    if match:
                        flight_info['aircraft_type'] = match.group(1).strip()
        
        driver.quit()
        return flight_info
    
    except Exception as e:
        print(f"Error fetching data: {e}")
        driver.quit()
        return None