from app import db
from models import AirlineData
from datetime import datetime, timedelta
import logging
from sqlalchemy import func

def process_airline_data(data_records):
    """
    Process raw airline data records into structured format for analysis
    """
    processed_data = []
    
    try:
        for record in data_records:
            processed_record = {
                'id': record.id,
                'route': record.route,
                'origin': record.origin,
                'destination': record.destination,
                'price': record.price,
                'airline': record.airline,
                'departure_date': record.departure_date.strftime('%Y-%m-%d') if record.departure_date else None,
                'scraped_at': record.scraped_at.strftime('%Y-%m-%d %H:%M:%S') if record.scraped_at else None,
                'source_url': record.source_url
            }
            processed_data.append(processed_record)
        
        logging.info(f"Successfully processed {len(processed_data)} airline records")
        
    except Exception as e:
        logging.error(f"Error processing airline data: {str(e)}")
        raise e
    
    return processed_data

def get_popular_routes(limit=10):
    """
    Get the most popular routes based on booking frequency
    """
    try:
        popular_routes = db.session.query(
            AirlineData.route,
            AirlineData.origin,
            AirlineData.destination,
            func.count(AirlineData.id).label('booking_count'),
            func.avg(AirlineData.price).label('avg_price'),
            func.min(AirlineData.price).label('min_price'),
            func.max(AirlineData.price).label('max_price')
        ).group_by(
            AirlineData.route,
            AirlineData.origin,
            AirlineData.destination
        ).order_by(
            func.count(AirlineData.id).desc()
        ).limit(limit).all()
        
        result = []
        for route in popular_routes:
            result.append({
                'route': route.route,
                'origin': route.origin,
                'destination': route.destination,
                'booking_count': route.booking_count,
                'avg_price': round(route.avg_price, 2),
                'min_price': route.min_price,
                'max_price': route.max_price
            })
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting popular routes: {str(e)}")
        return []

def get_price_trends(days=30):
    """
    Get price trends over the specified number of days
    """
    try:
        # Get price data grouped by date
        cutoff_date = datetime.utcnow() - timedelta(days=days)
        
        price_trends = db.session.query(
            func.date(AirlineData.departure_date).label('date'),
            func.avg(AirlineData.price).label('avg_price'),
            func.count(AirlineData.id).label('booking_count')
        ).filter(
            AirlineData.departure_date >= cutoff_date
        ).group_by(
            func.date(AirlineData.departure_date)
        ).order_by(
            func.date(AirlineData.departure_date)
        ).all()
        
        result = []
        for trend in price_trends:
            # Handle both date objects and string dates
            if hasattr(trend.date, 'strftime'):
                formatted_date = trend.date.strftime('%Y-%m-%d')
            else:
                formatted_date = str(trend.date) if trend.date else None
                
            result.append({
                'date': formatted_date,
                'avg_price': round(trend.avg_price, 2),
                'booking_count': trend.booking_count
            })
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting price trends: {str(e)}")
        return []

def get_airline_performance():
    """
    Get performance statistics for each airline
    """
    try:
        airline_stats = db.session.query(
            AirlineData.airline,
            func.count(AirlineData.id).label('total_bookings'),
            func.avg(AirlineData.price).label('avg_price'),
            func.min(AirlineData.price).label('min_price'),
            func.max(AirlineData.price).label('max_price'),
            func.count(func.distinct(AirlineData.route)).label('route_count')
        ).group_by(
            AirlineData.airline
        ).order_by(
            func.count(AirlineData.id).desc()
        ).all()
        
        result = []
        total_bookings = sum(stat.total_bookings for stat in airline_stats)
        
        for stat in airline_stats:
            market_share = round((stat.total_bookings / total_bookings) * 100, 2) if total_bookings > 0 else 0
            
            result.append({
                'airline': stat.airline,
                'total_bookings': stat.total_bookings,
                'market_share': market_share,
                'avg_price': round(stat.avg_price, 2),
                'min_price': stat.min_price,
                'max_price': stat.max_price,
                'route_count': stat.route_count
            })
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting airline performance: {str(e)}")
        return []

def get_demand_by_month():
    """
    Get demand statistics grouped by month
    """
    try:
        monthly_demand = db.session.query(
            func.strftime('%Y-%m', AirlineData.departure_date).label('month'),
            func.count(AirlineData.id).label('booking_count'),
            func.avg(AirlineData.price).label('avg_price')
        ).group_by(
            func.strftime('%Y-%m', AirlineData.departure_date)
        ).order_by(
            func.strftime('%Y-%m', AirlineData.departure_date)
        ).all()
        
        result = []
        for demand in monthly_demand:
            result.append({
                'month': demand.month,
                'booking_count': demand.booking_count,
                'avg_price': round(demand.avg_price, 2)
            })
        
        return result
        
    except Exception as e:
        logging.error(f"Error getting demand by month: {str(e)}")
        return []

def get_route_statistics(route):
    """
    Get detailed statistics for a specific route
    """
    try:
        route_data = AirlineData.query.filter_by(route=route).all()
        
        if not route_data:
            return None
        
        prices = [record.price for record in route_data]
        airlines = list(set(record.airline for record in route_data))
        
        statistics = {
            'route': route,
            'total_bookings': len(route_data),
            'avg_price': round(sum(prices) / len(prices), 2),
            'min_price': min(prices),
            'max_price': max(prices),
            'price_std': round(calculate_standard_deviation(prices), 2),
            'airlines': airlines,
            'airline_count': len(airlines),
            'latest_price': route_data[-1].price if route_data else None,
            'oldest_record': route_data[0].scraped_at.strftime('%Y-%m-%d') if route_data else None,
            'latest_record': route_data[-1].scraped_at.strftime('%Y-%m-%d') if route_data else None
        }
        
        return statistics
        
    except Exception as e:
        logging.error(f"Error getting route statistics: {str(e)}")
        return None

def calculate_standard_deviation(values):
    """
    Calculate standard deviation for a list of values
    """
    if len(values) < 2:
        return 0
    
    mean = sum(values) / len(values)
    variance = sum((x - mean) ** 2 for x in values) / (len(values) - 1)
    return variance ** 0.5

def get_price_alerts(threshold_percentage=10):
    """
    Get price alerts for routes that have significant price changes
    """
    try:
        # Get recent price data (last 7 days vs previous 7 days)
        recent_date = datetime.utcnow() - timedelta(days=7)
        old_date = datetime.utcnow() - timedelta(days=14)
        
        # Get average prices for recent period
        recent_prices = db.session.query(
            AirlineData.route,
            func.avg(AirlineData.price).label('recent_avg_price')
        ).filter(
            AirlineData.departure_date >= recent_date
        ).group_by(
            AirlineData.route
        ).subquery()
        
        # Get average prices for previous period
        old_prices = db.session.query(
            AirlineData.route,
            func.avg(AirlineData.price).label('old_avg_price')
        ).filter(
            AirlineData.departure_date.between(old_date, recent_date)
        ).group_by(
            AirlineData.route
        ).subquery()
        
        # Join and calculate percentage change
        price_changes = db.session.query(
            recent_prices.c.route,
            recent_prices.c.recent_avg_price,
            old_prices.c.old_avg_price
        ).join(
            old_prices,
            recent_prices.c.route == old_prices.c.route
        ).all()
        
        alerts = []
        for change in price_changes:
            if change.old_avg_price and change.old_avg_price > 0:
                percentage_change = ((change.recent_avg_price - change.old_avg_price) / change.old_avg_price) * 100
                
                if abs(percentage_change) >= threshold_percentage:
                    alerts.append({
                        'route': change.route,
                        'old_price': round(change.old_avg_price, 2),
                        'new_price': round(change.recent_avg_price, 2),
                        'percentage_change': round(percentage_change, 2),
                        'alert_type': 'price_increase' if percentage_change > 0 else 'price_decrease'
                    })
        
        # Sort by absolute percentage change
        alerts.sort(key=lambda x: abs(x['percentage_change']), reverse=True)
        
        return alerts
        
    except Exception as e:
        logging.error(f"Error getting price alerts: {str(e)}")
        return []
