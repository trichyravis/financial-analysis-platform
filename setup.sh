#!/bin/bash
# Setup script for Mac/Linux

echo "🏔️ The Mountain Path - Financial Analysis Platform"
echo "Setting up your system..."

# Check Python version
python3 --version

# Create virtual environment
echo "📦 Creating virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "🔧 Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "📥 Installing dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

echo "✅ Setup complete!"
echo ""
echo "🚀 To launch the application, run:"
echo "   source venv/bin/activate"
echo "   streamlit run app.py"
echo ""
echo "Happy analyzing! 🎉"
