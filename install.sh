#!/bin/bash

echo "=== Airline Market Analytics Installation ==="
echo

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "Error: Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "Error: pip3 is not installed. Please install pip3."
    exit 1
fi

# Install dependencies
echo "Installing Python dependencies..."
pip3 install -r requirements.txt

# Create instance directory if it doesn't exist
mkdir -p instance

# Set up environment variables
echo
echo "Setting up environment variables..."
echo "Please set the following environment variables:"
echo "export OPENAI_API_KEY='your_openai_api_key'"
echo "export SESSION_SECRET='your_session_secret'"
echo "export DATABASE_URL='sqlite:///instance/airline_data.db'"
echo

# Initialize database with sample data
echo "Initializing database with sample data..."
python3 populate_sample_data.py

echo
echo "Installation complete!"
echo "To run the application:"
echo "1. Set your environment variables (especially OPENAI_API_KEY)"
echo "2. Run: python3 run.py"
echo "3. Open your browser to: http://localhost:5000"
echo