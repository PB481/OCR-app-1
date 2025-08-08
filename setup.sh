#!/usr/bin/env bash

# Heroku setup script for Fund Administration Platform

# Install system dependencies
apt-get update -qq && apt-get install -y \
    build-essential \
    curl \
    software-properties-common \
    git \
    && rm -rf /var/lib/apt/lists/*

# Install Python dependencies
pip install -r requirements.txt

# Create necessary directories
mkdir -p ~/.streamlit/

# Create Streamlit config
cat > ~/.streamlit/config.toml << EOF
[server]
headless = true
enableCORS = false
port = \$PORT

[browser]
gatherUsageStats = false
EOF 