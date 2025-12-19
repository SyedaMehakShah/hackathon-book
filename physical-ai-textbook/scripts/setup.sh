#!/bin/bash
# setup.sh - One command setup script for the Physical AI & Humanoid Robotics textbook

set -e  # Exit immediately if a command exits with a non-zero status

echo "==========================================="
echo "Physical AI & Humanoid Robotics Textbook Setup"
echo "==========================================="

# Check if Node.js is installed
if ! command -v node &> /dev/null; then
    echo "❌ Node.js is not installed. Please install Node.js 18.x or higher."
    exit 1
fi

# Check Node.js version
NODE_VERSION=$(node -v | cut -d'v' -f2)
NODE_MAJOR=$(echo $NODE_VERSION | cut -d'.' -f1)
if [ "$NODE_MAJOR" -lt 18 ]; then
    echo "❌ Node.js version $NODE_VERSION is too old. Please install Node.js 18.x or higher."
    exit 1
fi

# Check if Python is installed
if ! command -v python &> /dev/null && ! command -v python3 &> /dev/null; then
    echo "❌ Python is not installed. Please install Python 3.9 or higher."
    exit 1
fi

# Use python3 if python command doesn't exist
PYTHON_CMD="python"
if ! command -v python &> /dev/null; then
    PYTHON_CMD="python3"
fi

# Check Python version
PYTHON_VERSION=$($PYTHON_CMD --version 2>&1 | cut -d' ' -f2)
PYTHON_MAJOR=$(echo $PYTHON_VERSION | cut -d'.' -f1)
PYTHON_MINOR=$(echo $PYTHON_VERSION | cut -d'.' -f2)
if [ "$PYTHON_MAJOR" -lt 3 ] || ([ "$PYTHON_MAJOR" -eq 3 ] && [ "$PYTHON_MINOR" -lt 9 ]); then
    echo "❌ Python version $PYTHON_VERSION is too old. Please install Python 3.9 or higher."
    exit 1
fi

echo "✅ Node.js version $NODE_VERSION detected"
echo "✅ Python version $PYTHON_VERSION detected"

# Navigate to the project directory
PROJECT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$PROJECT_DIR/.."

echo "📍 Working in directory: $(pwd)"

# Install frontend dependencies
echo "📦 Installing frontend dependencies..."
npm install

# Create virtual environment and install Python dependencies
echo "🐍 Setting up Python virtual environment..."
$PYTHON_CMD -m venv api/venv

# Activate virtual environment
source api/venv/bin/activate

# Upgrade pip
pip install --upgrade pip

# Install Python dependencies
echo "📦 Installing Python dependencies..."
cd api
pip install -r requirements.txt

# Come back to the root directory
cd ..

# Check if .env file exists, if not create from .env.example
if [ ! -f .env ]; then
    echo "📝 Creating .env file from .env.example..."
    cp .env.example .env
    echo "⚠️  Please update the .env file with your actual configuration before running the application"
fi

# Create uploads directory for any file uploads
mkdir -p api/uploads

# Build the Docusaurus project
echo "🔨 Building Docusaurus project..."
npm run build

echo "==========================================="
echo "✅ Setup completed successfully!"
echo "==========================================="
echo ""
echo "To run the application:"
echo "1. Start the backend: cd api && source venv/bin/activate && python -m uvicorn main:app --reload"
echo "2. In a new terminal, start the frontend: npm run start"
echo ""
echo "To run both simultaneously, use: npm start"
echo ""
echo "For more information, check the README.md file."