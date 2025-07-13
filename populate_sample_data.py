"""
Script to populate the database with sample airline data for testing
"""

from app import app, db
from models import AirlineData, ScrapingLog
from datetime import datetime, timedelta
import random

def populate_sample_data():
    """Generate and insert sample airline data into the database"""
    
    with app.app_context():
        # Clear existing data
        AirlineData.query.delete()
        ScrapingLog.query.delete()
        
        airlines = ['United', 'American', 'Delta', 'Southwest', 'JetBlue', 'Alaska', 'Spirit', 'Frontier']
        
        # Common US routes with realistic price ranges
        routes = [
            ('LAX', 'JFK', 'Los Angeles', 'New York', 300, 600),
            ('SFO', 'BOS', 'San Francisco', 'Boston', 350, 650),
            ('CHI', 'MIA', 'Chicago', 'Miami', 250, 500),
            ('DEN', 'SEA', 'Denver', 'Seattle', 200, 450),
            ('ATL', 'LAS', 'Atlanta', 'Las Vegas', 180, 400),
            ('DFW', 'PHX', 'Dallas', 'Phoenix', 150, 350),
            ('MSP', 'PDX', 'Minneapolis', 'Portland', 300, 550),
            ('DTW', 'SAN', 'Detroit', 'San Diego', 350, 650),
            ('PHL', 'SLC', 'Philadelphia', 'Salt Lake City', 400, 700),
            ('IAH', 'MCO', 'Houston', 'Orlando', 200, 450),
            ('BOS', 'LAX', 'Boston', 'Los Angeles', 350, 650),
            ('MIA', 'SFO', 'Miami', 'San Francisco', 400, 750),
            ('LAS', 'JFK', 'Las Vegas', 'New York', 250, 500),
            ('PHX', 'CHI', 'Phoenix', 'Chicago', 200, 450),
            ('SEA', 'ATL', 'Seattle', 'Atlanta', 300, 550)
        ]
        
        # Generate sample data for the past 60 days
        start_date = datetime.now() - timedelta(days=60)
        
        sample_data = []
        for _ in range(500):  # Generate 500 sample records
            route_info = random.choice(routes)
            origin_code, dest_code, origin_name, dest_name, min_price, max_price = route_info
            
            price = round(random.uniform(min_price, max_price), 2)
            airline = random.choice(airlines)
            
            # Generate random departure date within next 90 days
            departure_date = datetime.now() + timedelta(days=random.randint(1, 90))
            
            # Generate random scraped_at date within past 60 days
            scraped_at = start_date + timedelta(days=random.randint(0, 59))
            
            flight_record = AirlineData(
                route=f"{origin_code} → {dest_code}",
                origin=origin_code,
                destination=dest_code,
                price=price,
                airline=airline,
                departure_date=departure_date,
                scraped_at=scraped_at,
                source_url=f"https://example-travel-site.com/flights/{origin_code}-{dest_code}"
            )
            
            sample_data.append(flight_record)
        
        # Bulk insert the data
        db.session.bulk_save_objects(sample_data)
        
        # Add some scraping log entries
        sources = ['https://www.kayak.com/flights', 'https://www.expedia.com/Flights', 'https://www.skyscanner.com']
        for source in sources:
            log_entry = ScrapingLog(
                source=source,
                status='success',
                records_scraped=random.randint(150, 200),
                scraped_at=datetime.now() - timedelta(minutes=random.randint(10, 60))
            )
            db.session.add(log_entry)
        
        db.session.commit()
        print(f"Successfully populated database with {len(sample_data)} sample flight records")

if __name__ == '__main__':
    populate_sample_data()