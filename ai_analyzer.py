import json
import os
from openai import OpenAI
import logging
from datetime import datetime

# the newest OpenAI model is "gpt-4o" which was released May 13, 2024.
# do not change this unless explicitly requested by the user
OPENAI_API_KEY = os.environ.get("OPENAI_API_KEY", "default_key")
openai = OpenAI(api_key=OPENAI_API_KEY)

def analyze_market_trends(processed_data):
    """
    Analyze airline market data using OpenAI to generate insights
    Returns a dictionary with different types of insights
    """
    insights = {}
    
    try:
        # Analyze popular routes
        insights['popular_routes'] = analyze_popular_routes(processed_data)
        
        # Analyze price trends
        insights['price_trends'] = analyze_price_trends(processed_data)
        
        # Analyze demand patterns
        insights['demand_analysis'] = analyze_demand_patterns(processed_data)
        
        logging.info("Successfully generated market insights")
        
    except Exception as e:
        logging.error(f"Error analyzing market trends: {str(e)}")
        raise e
    
    return insights

def analyze_popular_routes(data):
    """
    Analyze popular routes using OpenAI
    """
    try:
        # Prepare data summary for analysis
        route_summary = prepare_route_summary(data)
        
        prompt = f"""
        Analyze the following airline route data and provide insights about popular routes:
        
        Data: {route_summary}
        
        Please provide analysis in JSON format with the following structure:
        {{
            "top_routes": [
                {{
                    "route": "route name",
                    "popularity_score": number,
                    "avg_price": number,
                    "trend": "increasing/decreasing/stable"
                }}
            ],
            "insights": [
                "insight 1",
                "insight 2",
                "insight 3"
            ],
            "recommendations": [
                "recommendation 1",
                "recommendation 2"
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert airline market analyst. Analyze the provided data and give actionable insights about popular routes, pricing trends, and market demand."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error analyzing popular routes: {str(e)}")
        return json.dumps({"error": f"Failed to analyze popular routes: {str(e)}"})

def analyze_price_trends(data):
    """
    Analyze price trends using OpenAI
    """
    try:
        # Prepare price data for analysis
        price_summary = prepare_price_summary(data)
        
        prompt = f"""
        Analyze the following airline pricing data and provide insights about price trends:
        
        Data: {price_summary}
        
        Please provide analysis in JSON format with the following structure:
        {{
            "overall_trend": "increasing/decreasing/stable",
            "price_ranges": {{
                "budget": {{"min": number, "max": number}},
                "mid_range": {{"min": number, "max": number}},
                "premium": {{"min": number, "max": number}}
            }},
            "seasonal_patterns": [
                {{
                    "period": "period name",
                    "price_change": "percentage change",
                    "reason": "explanation"
                }}
            ],
            "insights": [
                "insight 1",
                "insight 2",
                "insight 3"
            ],
            "recommendations": [
                "recommendation 1",
                "recommendation 2"
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert airline pricing analyst. Analyze the provided data and give actionable insights about pricing trends, seasonal patterns, and market dynamics."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error analyzing price trends: {str(e)}")
        return json.dumps({"error": f"Failed to analyze price trends: {str(e)}"})

def analyze_demand_patterns(data):
    """
    Analyze demand patterns using OpenAI
    """
    try:
        # Prepare demand data for analysis
        demand_summary = prepare_demand_summary(data)
        
        prompt = f"""
        Analyze the following airline demand data and provide insights about market demand patterns:
        
        Data: {demand_summary}
        
        Please provide analysis in JSON format with the following structure:
        {{
            "peak_demand_periods": [
                {{
                    "period": "period name",
                    "demand_level": "high/medium/low",
                    "key_routes": ["route1", "route2"],
                    "reasons": ["reason1", "reason2"]
                }}
            ],
            "airline_performance": [
                {{
                    "airline": "airline name",
                    "market_share": "percentage",
                    "growth_trend": "increasing/decreasing/stable",
                    "competitive_advantage": "description"
                }}
            ],
            "market_opportunities": [
                {{
                    "opportunity": "opportunity description",
                    "potential_impact": "high/medium/low",
                    "recommendation": "action to take"
                }}
            ],
            "insights": [
                "insight 1",
                "insight 2",
                "insight 3"
            ]
        }}
        """
        
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[
                {
                    "role": "system",
                    "content": "You are an expert airline demand analyst. Analyze the provided data and give actionable insights about market demand patterns, airline performance, and business opportunities."
                },
                {"role": "user", "content": prompt}
            ],
            response_format={"type": "json_object"}
        )
        
        return response.choices[0].message.content
        
    except Exception as e:
        logging.error(f"Error analyzing demand patterns: {str(e)}")
        return json.dumps({"error": f"Failed to analyze demand patterns: {str(e)}"})

def prepare_route_summary(data):
    """
    Prepare route data summary for AI analysis
    """
    try:
        route_stats = {}
        
        for record in data:
            route = record['route']
            if route not in route_stats:
                route_stats[route] = {
                    'count': 0,
                    'total_price': 0,
                    'airlines': set(),
                    'origins': set(),
                    'destinations': set()
                }
            
            route_stats[route]['count'] += 1
            route_stats[route]['total_price'] += record['price']
            route_stats[route]['airlines'].add(record['airline'])
            route_stats[route]['origins'].add(record['origin'])
            route_stats[route]['destinations'].add(record['destination'])
        
        # Convert to serializable format
        summary = []
        for route, stats in route_stats.items():
            summary.append({
                'route': route,
                'booking_count': stats['count'],
                'avg_price': round(stats['total_price'] / stats['count'], 2),
                'airline_count': len(stats['airlines']),
                'airlines': list(stats['airlines'])
            })
        
        # Sort by booking count
        summary.sort(key=lambda x: x['booking_count'], reverse=True)
        
        return summary[:20]  # Top 20 routes
        
    except Exception as e:
        logging.error(f"Error preparing route summary: {str(e)}")
        return []

def prepare_price_summary(data):
    """
    Prepare price data summary for AI analysis
    """
    try:
        price_data = []
        
        for record in data:
            price_data.append({
                'route': record['route'],
                'price': record['price'],
                'airline': record['airline'],
                'departure_date': record['departure_date'],
                'month': record['departure_date'][:7]  # YYYY-MM format
            })
        
        # Calculate price statistics by route and month
        price_stats = {}
        for record in price_data:
            key = f"{record['route']}_{record['month']}"
            if key not in price_stats:
                price_stats[key] = {
                    'route': record['route'],
                    'month': record['month'],
                    'prices': []
                }
            price_stats[key]['prices'].append(record['price'])
        
        # Calculate averages
        summary = []
        for key, stats in price_stats.items():
            prices = stats['prices']
            summary.append({
                'route': stats['route'],
                'month': stats['month'],
                'avg_price': round(sum(prices) / len(prices), 2),
                'min_price': min(prices),
                'max_price': max(prices),
                'price_count': len(prices)
            })
        
        return summary
        
    except Exception as e:
        logging.error(f"Error preparing price summary: {str(e)}")
        return []

def prepare_demand_summary(data):
    """
    Prepare demand data summary for AI analysis
    """
    try:
        demand_data = {
            'total_bookings': len(data),
            'airlines': {},
            'routes': {},
            'monthly_demand': {}
        }
        
        for record in data:
            # Airline statistics
            airline = record['airline']
            if airline not in demand_data['airlines']:
                demand_data['airlines'][airline] = {
                    'booking_count': 0,
                    'total_revenue': 0,
                    'avg_price': 0,
                    'routes': set()
                }
            
            demand_data['airlines'][airline]['booking_count'] += 1
            demand_data['airlines'][airline]['total_revenue'] += record['price']
            demand_data['airlines'][airline]['routes'].add(record['route'])
            
            # Route statistics
            route = record['route']
            if route not in demand_data['routes']:
                demand_data['routes'][route] = {
                    'booking_count': 0,
                    'avg_price': 0,
                    'airlines': set()
                }
            
            demand_data['routes'][route]['booking_count'] += 1
            demand_data['routes'][route]['airlines'].add(airline)
            
            # Monthly demand
            month = record['departure_date'][:7]
            if month not in demand_data['monthly_demand']:
                demand_data['monthly_demand'][month] = 0
            demand_data['monthly_demand'][month] += 1
        
        # Calculate averages and convert sets to lists
        for airline in demand_data['airlines']:
            stats = demand_data['airlines'][airline]
            stats['avg_price'] = round(stats['total_revenue'] / stats['booking_count'], 2)
            stats['routes'] = list(stats['routes'])
        
        for route in demand_data['routes']:
            stats = demand_data['routes'][route]
            stats['airlines'] = list(stats['airlines'])
        
        return demand_data
        
    except Exception as e:
        logging.error(f"Error preparing demand summary: {str(e)}")
        return {}
