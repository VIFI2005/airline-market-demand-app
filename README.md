Airline Market Analytics

A Flask web application that scrapes airline booking data, processes it with AI insights, and provides interactive visualizations of market demand trends.

Features

- **Data Scraping**: Automated collection of airline pricing data from multiple sources
- **AI Analysis**: OpenAI-powered insights for market trends and demand patterns
- **Interactive Dashboard**: Real-time charts and data visualization
- **Data Filtering**: Advanced search and filtering capabilities
- **Market Insights**: AI-generated analysis of popular routes, price trends, and demand

Installation

1. Clone or extract the project files
2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

3. Set up environment variables:
   ```bash
   export OPENAI_API_KEY="your_openai_api_key"
   export SESSION_SECRET="your_session_secret"
   export DATABASE_URL="sqlite:///instance/airline_data.db"
   ```

4. Initialize the database:
   ```bash
   python populate_sample_data.py
   ```

5. Run the application:
   ```bash
   python main.py
   ```

Usage

1. **Dashboard**: View overview of flight data, charts, and statistics
2. **Data Scraping**: Click "Scrape Data" to collect new flight information
3. **AI Insights**: Generate AI-powered market analysis
4. **Filtering**: Use the filter form to search for specific routes or airlines

Project Structure

- `app.py`: Main Flask application setup
- `main.py`: Application entry point
- `models.py`: Database models
- `routes.py`: Flask routes and API endpoints
- `data_scraper.py`: Web scraping functionality
- `ai_analyzer.py`: OpenAI integration for insights
- `data_processor.py`: Data processing utilities
- `templates/`: HTML templates
- `static/`: CSS and JavaScript files
- `instance/`: Database files

Configuration

Environment Variables

- `Gemini AI`: Your OpenAI API key for AI insights
- `SESSION_SECRET`: Flask session secret key
- `DATABASE_URL`: Database connection string (default: SQLite)

Database

The application uses SQLite by default. For production, you can use PostgreSQL by setting the `DATABASE_URL` environment variable.

API Endpoints

- `GET /`: Main dashboard
- `POST /scrape-data`: Trigger data scraping
- `POST /generate-insights`: Generate AI insights
- `GET /insights`: View AI insights
- `GET /api/chart-data/<chart_type>`: Chart data API
- `GET /api/filter-data`: Filter flight data

Dependencies

- Flask 3.0.0
- Flask-SQLAlchemy 3.1.1
- OpenAI 1.51.2
- Requests 2.31.0
- BeautifulSoup4 4.12.2
- Trafilatura 1.12.2
- Gunicorn 21.2.0

License

This project is for educational and demonstration purposes.



