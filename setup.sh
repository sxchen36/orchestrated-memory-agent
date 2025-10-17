#!/bin/bash
# Setup script for Hello World AI Agent

echo "🚀 Setting up Hello World AI Agent..."

# Check if virtual environment exists
if [ ! -d "venv" ]; then
    echo "📦 Creating virtual environment..."
    python3 -m venv venv
fi

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install -r requirements.txt

# Check if .env file exists
if [ ! -f ".env" ]; then
    echo "⚠️  Please create a .env file with your OpenAI API key:"
    echo "   OPENAI_API_KEY=your_api_key_here"
    echo ""
fi

echo "✅ Setup complete!"
echo "To run the agent:"
echo "   source venv/bin/activate"
echo "   python main.py"
