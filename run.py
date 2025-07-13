#!/usr/bin/env python3
"""
Run script for Airline Market Analytics
"""

import os
import sys
from app import app

if __name__ == '__main__':
    # Set default environment variables if not set
    if not os.environ.get('SESSION_SECRET'):
        os.environ['SESSION_SECRET'] = 'your-secret-key-change-this-in-production'
    
    if not os.environ.get('DATABASE_URL'):
        os.environ['DATABASE_URL'] = 'sqlite:///instance/airline_data.db'
    
    # Check if OpenAI API key is set
    if not os.environ.get('OPENAI_API_KEY'):
        print("Warning: OPENAI_API_KEY environment variable not set.")
        print("AI insights will not work without a valid OpenAI API key.")
        print("Set it with: export OPENAI_API_KEY='your-key-here'")
        print()
    
    # Run the Flask app
    print("Starting Airline Market Analytics...")
    print("Access the application at: http://localhost:5000")
    print("Press Ctrl+C to stop the server")
    
    app.run(
        host='0.0.0.0',
        port=5000,
        debug=True
    )