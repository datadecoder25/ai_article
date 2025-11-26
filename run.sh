#!/bin/bash

# Quick Start Script for Article Generator
# This script helps you set up and run the article generator quickly

echo "=================================="
echo "ML Article Generator - Quick Start"
echo "=================================="
echo ""

# Check if Python is installed
if ! command -v python3 &> /dev/null; then
    echo "❌ Python 3 is not installed. Please install Python 3.8 or higher."
    exit 1
fi

echo "✅ Python 3 found"

# Check if pip is installed
if ! command -v pip3 &> /dev/null; then
    echo "❌ pip3 is not installed. Please install pip3."
    exit 1
fi

echo "✅ pip3 found"

# Install dependencies
echo ""
echo "📦 Installing dependencies..."
pip3 install -r requirements.txt

# Check if call_llm.py exists
echo ""
if [ ! -f "call_llm.py" ]; then
    echo "⚠️  call_llm.py not found. Make sure it's in the same directory."
    exit 1
else
    echo "✅ call_llm.py found"
fi

# Check if topics.json exists
echo ""
if [ ! -f "topics.json" ]; then
    echo "⚠️  topics.json not found. Please create one or use the sample."
    exit 1
else
    echo "✅ topics.json found"
fi

# Run the generator
echo ""
echo "🚀 Running article generator..."
echo ""
python3 article_generator.py "$@"

echo ""
echo "=================================="
echo "Done! Check the generated SQL file."
echo "=================================="

