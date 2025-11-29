#!/bin/bash
# Launch script for Chess.com Analytics Dashboard

echo "🚀 Starting Chess.com Analytics Dashboard..."
echo ""

# Activate virtual environment
source venv/bin/activate

# Run Streamlit app
streamlit run app.py --server.port 8501 --server.address 0.0.0.0
