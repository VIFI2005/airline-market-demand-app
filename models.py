from app import db
from datetime import datetime
from sqlalchemy import Text, Float, Integer, String, DateTime

class AirlineData(db.Model):
    id = db.Column(Integer, primary_key=True)
    route = db.Column(String(200), nullable=False)
    origin = db.Column(String(100), nullable=False)
    destination = db.Column(String(100), nullable=False)
    price = db.Column(Float, nullable=False)
    airline = db.Column(String(100), nullable=False)
    departure_date = db.Column(DateTime, nullable=False)
    scraped_at = db.Column(DateTime, default=datetime.utcnow)
    source_url = db.Column(String(500))
    
    def __repr__(self):
        return f'<AirlineData {self.route}: ${self.price}>'

class MarketInsight(db.Model):
    id = db.Column(Integer, primary_key=True)
    insight_type = db.Column(String(100), nullable=False)  # 'popular_routes', 'price_trends', 'demand_analysis'
    content = db.Column(Text, nullable=False)
    generated_at = db.Column(DateTime, default=datetime.utcnow)
    data_period_start = db.Column(DateTime, nullable=False)
    data_period_end = db.Column(DateTime, nullable=False)
    
    def __repr__(self):
        return f'<MarketInsight {self.insight_type}>'

class ScrapingLog(db.Model):
    id = db.Column(Integer, primary_key=True)
    source = db.Column(String(200), nullable=False)
    status = db.Column(String(50), nullable=False)  # 'success', 'error', 'partial'
    records_scraped = db.Column(Integer, default=0)
    error_message = db.Column(Text)
    scraped_at = db.Column(DateTime, default=datetime.utcnow)
    
    def __repr__(self):
        return f'<ScrapingLog {self.source}: {self.status}>'
