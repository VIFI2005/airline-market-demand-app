# Airline Market Analytics

## Overview

This is a Flask-based web application that scrapes airline pricing data from various sources, processes it using AI-powered analysis, and provides market insights through an interactive dashboard. The application combines web scraping, data processing, OpenAI integration, and data visualization to deliver actionable intelligence about airline market trends.

## User Preferences

Preferred communication style: Simple, everyday language.

## System Architecture

The application follows a traditional three-tier architecture with a Flask backend, SQLAlchemy ORM for data persistence, and a responsive Bootstrap frontend. The system is designed around four main functional components: data scraping, data processing, AI analysis, and web presentation.

### Core Architecture Decisions:

1. **Flask Framework**: Chosen for its simplicity and rapid development capabilities, suitable for a data analytics application
2. **SQLite Database**: Selected for development simplicity and ease of deployment on Replit
3. **OpenAI Integration**: Leverages GPT-4o for advanced market trend analysis and insights generation
4. **Bootstrap Frontend**: Provides responsive, professional UI with dark theme optimized for data visualization

## Key Components

### Backend Components

1. **app.py**: Main Flask application setup with database configuration and initialization
2. **models.py**: SQLAlchemy models defining the data schema:
   - `AirlineData`: Stores scraped flight pricing data
   - `MarketInsight`: Stores AI-generated market analysis
   - `ScrapingLog`: Tracks scraping operations and status

3. **routes.py**: Flask routes handling web requests and API endpoints
4. **data_scraper.py**: Web scraping module for collecting airline data from multiple sources
5. **data_processor.py**: Data processing utilities for cleaning and aggregating scraped data
6. **ai_analyzer.py**: OpenAI integration for generating market insights and trend analysis

### Frontend Components

1. **templates/**: Jinja2 templates for web interface
   - `base.html`: Base template with navigation and Bootstrap setup
   - `index.html`: Main dashboard with statistics and charts
   - `insights.html`: AI insights display page

2. **static/**: Frontend assets
   - `css/style.css`: Custom styling for enhanced user experience
   - `js/charts.js`: Chart.js integration for data visualization
   - `js/main.js`: Main frontend JavaScript functionality

## Data Flow

1. **Data Collection**: Web scraping modules collect airline pricing data from multiple sources (Kayak, Expedia, Skyscanner)
2. **Data Storage**: Raw data is stored in SQLite database via SQLAlchemy ORM
3. **Data Processing**: Data processor cleans and aggregates the raw data for analysis
4. **AI Analysis**: OpenAI API analyzes processed data to generate market insights
5. **Visualization**: Frontend displays processed data and insights through interactive charts and tables

## External Dependencies

### Core Dependencies:
- **Flask**: Web framework and application server
- **SQLAlchemy**: ORM for database operations
- **OpenAI**: AI analysis and insights generation
- **Bootstrap**: Frontend UI framework
- **Chart.js**: Data visualization library
- **Feather Icons**: Icon system for UI elements

### Web Scraping Dependencies:
- **Requests**: HTTP client for web scraping
- **BeautifulSoup**: HTML parsing and extraction
- **Trafilatura**: Web content extraction

## Deployment Strategy

The application is configured for deployment on Replit with the following considerations:

1. **Development Mode**: Flask runs in debug mode with auto-reload
2. **Database**: SQLite database with automatic table creation
3. **Environment Variables**: OpenAI API key configuration via environment variables
4. **Static Assets**: CDN-hosted Bootstrap, Chart.js, and Feather Icons for reliability
5. **WSGI Configuration**: ProxyFix middleware for proper request handling

### Configuration Files:
- **main.py**: Entry point for Replit deployment
- **app.py**: Main application configuration with database setup
- Environment variables required:
  - `OPENAI_API_KEY`: OpenAI API key for AI analysis
  - `SESSION_SECRET`: Flask session secret key

The architecture supports easy scaling and modification, with clear separation of concerns between data collection, processing, analysis, and presentation layers.