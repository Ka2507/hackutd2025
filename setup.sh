#!/bin/bash

# ProdigyPM Setup Script
echo "🚀 Setting up ProdigyPM..."

# Colors
GREEN='\033[0;32m'
BLUE='\033[0;34m'
YELLOW='\033[1;33m'
NC='\033[0m' # No Color

# Check Python
echo -e "\n${BLUE}Checking Python...${NC}"
if command -v python3 &> /dev/null; then
    PYTHON_VERSION=$(python3 --version)
    echo -e "${GREEN}✓ Found $PYTHON_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Python 3 not found. Please install Python 3.10+${NC}"
    exit 1
fi

# Check Node.js
echo -e "\n${BLUE}Checking Node.js...${NC}"
if command -v node &> /dev/null; then
    NODE_VERSION=$(node --version)
    echo -e "${GREEN}✓ Found Node.js $NODE_VERSION${NC}"
else
    echo -e "${YELLOW}⚠ Node.js not found. Please install Node.js 18+${NC}"
    exit 1
fi

# Setup Backend
echo -e "\n${BLUE}Setting up Backend...${NC}"
cd backend

# Create virtual environment
echo "Creating Python virtual environment..."
python3 -m venv venv

# Activate virtual environment
echo "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
echo "Installing Python dependencies..."
pip install --upgrade pip
pip install -r requirements.txt

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating backend .env file..."
    cp .env.example .env
    echo -e "${YELLOW}⚠ Please edit backend/.env with your API keys${NC}"
fi

# Create necessary directories
mkdir -p logs db

echo -e "${GREEN}✓ Backend setup complete${NC}"

# Setup Frontend
echo -e "\n${BLUE}Setting up Frontend...${NC}"
cd ../frontend

# Install dependencies
echo "Installing npm dependencies..."
npm install

# Create .env if it doesn't exist
if [ ! -f .env ]; then
    echo "Creating frontend .env file..."
    cp .env.example .env
fi

echo -e "${GREEN}✓ Frontend setup complete${NC}"

# Summary
echo -e "\n${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"
echo -e "${GREEN}✓ ProdigyPM Setup Complete!${NC}"
echo -e "${GREEN}━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━${NC}"

echo -e "\n${BLUE}Next Steps:${NC}"
echo -e "1. (Optional) Edit backend/.env with your API keys"
echo -e "2. (Optional) Install Ollama: ${YELLOW}curl https://ollama.ai/install.sh | sh${NC}"
echo -e "3. (Optional) Pull a model: ${YELLOW}ollama pull llama3:8b${NC}"
echo -e "\n${BLUE}To start the application:${NC}"
echo -e "  Backend:  ${YELLOW}cd backend && source venv/bin/activate && python main.py${NC}"
echo -e "  Frontend: ${YELLOW}cd frontend && npm run dev${NC}"
echo -e "\nThen open ${YELLOW}http://localhost:5173${NC} in your browser"
echo -e "\n${GREEN}Happy building! 🚀${NC}\n"

