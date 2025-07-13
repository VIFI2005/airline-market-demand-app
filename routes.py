from flask import render_template, request, jsonify, flash, redirect, url_for
from app import app, db
from models import AirlineData, MarketInsight, ScrapingLog
from data_scraper import scrape_airline_data
from ai_analyzer import analyze_market_trends
from data_processor import process_airline_data, get_popular_routes, get_price_trends
from datetime import datetime, timedelta
import logging

@app.route('/')
def index():
    """Main dashboard showing overview of airline market data"""
    # Get recent data stats
    total_records = AirlineData.query.count()
    recent_records = AirlineData.query.filter(
        AirlineData.scraped_at >= datetime.utcnow() - timedelta(days=7)
    ).count()
    
    # Get latest insights
    latest_insights = MarketInsight.query.order_by(
        MarketInsight.generated_at.desc()
    ).limit(3).all()
    
    # Get popular routes
    popular_routes = get_popular_routes(limit=10)
    
    return render_template('index.html', 
                         total_records=total_records,
                         recent_records=recent_records,
                         latest_insights=latest_insights,
                         popular_routes=popular_routes)

@app.route('/scrape-data', methods=['POST'])
def scrape_data():
    """Endpoint to trigger data scraping"""
    try:
        # Scrape data from multiple sources
        sources = [
            'https://www.kayak.com/flights',
            'https://www.expedia.com/Flights',
            'https://www.skyscanner.com'
        ]
        
        total_scraped = 0
        for source in sources:
            try:
                scraped_count = scrape_airline_data(source)
                total_scraped += scraped_count
                
                # Log successful scraping
                log_entry = ScrapingLog(
                    source=source,
                    status='success',
                    records_scraped=scraped_count
                )
                db.session.add(log_entry)
                
            except Exception as e:
                logging.error(f"Error scraping {source}: {str(e)}")
                log_entry = ScrapingLog(
                    source=source,
                    status='error',
                    error_message=str(e)
                )
                db.session.add(log_entry)
        
        db.session.commit()
        flash(f'Successfully scraped {total_scraped} records from {len(sources)} sources', 'success')
        
    except Exception as e:
        flash(f'Error during scraping: {str(e)}', 'error')
        logging.error(f"Scraping error: {str(e)}")
    
    return redirect(url_for('index'))

@app.route('/generate-insights', methods=['POST'])
def generate_insights():
    """Generate AI-powered market insights"""
    try:
        # Get recent data for analysis
        recent_data = AirlineData.query.filter(
            AirlineData.scraped_at >= datetime.utcnow() - timedelta(days=30)
        ).all()
        
        if not recent_data:
            flash('No recent data available for analysis', 'warning')
            return redirect(url_for('index'))
        
        # Process data and generate insights
        processed_data = process_airline_data(recent_data)
        insights = analyze_market_trends(processed_data)
        
        # Save insights to database
        for insight_type, content in insights.items():
            insight = MarketInsight(
                insight_type=insight_type,
                content=content,
                data_period_start=datetime.utcnow() - timedelta(days=30),
                data_period_end=datetime.utcnow()
            )
            db.session.add(insight)
        
        db.session.commit()
        flash('Market insights generated successfully', 'success')
        
    except Exception as e:
        flash(f'Error generating insights: {str(e)}', 'error')
        logging.error(f"Insight generation error: {str(e)}")
    
    return redirect(url_for('insights'))

@app.route('/insights')
def insights():
    """Show AI-generated market insights"""
    # Get all insights grouped by type
    insights_data = {}
    insight_types = ['popular_routes', 'price_trends', 'demand_analysis']
    
    for insight_type in insight_types:
        latest_insight = MarketInsight.query.filter_by(
            insight_type=insight_type
        ).order_by(MarketInsight.generated_at.desc()).first()
        
        if latest_insight:
            insights_data[insight_type] = latest_insight.content
    
    return render_template('insights.html', insights=insights_data)

@app.route('/api/chart-data/<chart_type>')
def chart_data(chart_type):
    """API endpoint to provide chart data"""
    try:
        if chart_type == 'price_trends':
            data = get_price_trends()
        elif chart_type == 'popular_routes':
            data = get_popular_routes(limit=20)
        elif chart_type == 'demand_by_month':
            # Get demand data by month
            data = db.session.query(
                db.func.strftime('%Y-%m', AirlineData.departure_date).label('month'),
                db.func.count(AirlineData.id).label('bookings')
            ).group_by(
                db.func.strftime('%Y-%m', AirlineData.departure_date)
            ).order_by('month').all()
            
            data = [{'month': row.month, 'bookings': row.bookings} for row in data]
        else:
            return jsonify({'error': 'Invalid chart type'}), 400
        
        return jsonify(data)
        
    except Exception as e:
        logging.error(f"Chart data error: {str(e)}")
        return jsonify({'error': str(e)}), 500

@app.route('/api/filter-data')
def filter_data():
    """API endpoint to filter airline data based on parameters"""
    try:
        # Get filter parameters
        origin = request.args.get('origin')
        destination = request.args.get('destination')
        airline = request.args.get('airline')
        min_price = request.args.get('min_price', type=float)
        max_price = request.args.get('max_price', type=float)
        date_from = request.args.get('date_from')
        date_to = request.args.get('date_to')
        
        # Build query
        query = AirlineData.query
        
        if origin:
            query = query.filter(AirlineData.origin.ilike(f'%{origin}%'))
        if destination:
            query = query.filter(AirlineData.destination.ilike(f'%{destination}%'))
        if airline:
            query = query.filter(AirlineData.airline.ilike(f'%{airline}%'))
        if min_price:
            query = query.filter(AirlineData.price >= min_price)
        if max_price:
            query = query.filter(AirlineData.price <= max_price)
        if date_from:
            query = query.filter(AirlineData.departure_date >= datetime.strptime(date_from, '%Y-%m-%d'))
        if date_to:
            query = query.filter(AirlineData.departure_date <= datetime.strptime(date_to, '%Y-%m-%d'))
        
        # Execute query and format results
        results = query.order_by(AirlineData.departure_date.desc()).limit(100).all()
        
        data = []
        for record in results:
            data.append({
                'route': record.route,
                'origin': record.origin,
                'destination': record.destination,
                'price': record.price,
                'airline': record.airline,
                'departure_date': record.departure_date.strftime('%Y-%m-%d'),
                'scraped_at': record.scraped_at.strftime('%Y-%m-%d %H:%M')
            })
        
        return jsonify(data)
        
    except Exception as e:
        logging.error(f"Filter data error: {str(e)}")
        return jsonify({'error': str(e)}), 500
