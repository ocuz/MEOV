#!/bin/bash

# Color codes for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}"
echo "╔════════════════════════════════════════════════════════╗"
echo "║     Username Sniper - Setup & Installation Script     ║"
echo "╚════════════════════════════════════════════════════════╝"
echo -e "${NC}"

# Check if Python is installed
echo -e "${YELLOW}[1/5]${NC} Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    echo -e "${RED}✗ Python 3 is not installed!${NC}"
    echo "Please install Python 3.8 or higher from https://www.python.org/"
    exit 1
fi

PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
echo -e "${GREEN}✓ Python ${PYTHON_VERSION} found${NC}"

# Check if pip is installed
echo -e "${YELLOW}[2/5]${NC} Checking pip installation..."
if ! command -v pip3 &> /dev/null; then
    echo -e "${RED}✗ pip is not installed!${NC}"
    echo "Please install pip or upgrade Python"
    exit 1
fi

echo -e "${GREEN}✓ pip found${NC}"

# Install requirements
echo -e "${YELLOW}[3/5]${NC} Installing Python dependencies..."
if pip3 install -r requirements.txt; then
    echo -e "${GREEN}✓ All dependencies installed successfully${NC}"
else
    echo -e "${RED}✗ Failed to install dependencies${NC}"
    exit 1
fi

# Setup environment file
echo -e "${YELLOW}[4/5]${NC} Setting up environment file..."
if [ ! -f .env ]; then
    if cp .env.example .env; then
        echo -e "${GREEN}✓ .env file created from template${NC}"
        echo -e "${YELLOW}⚠ IMPORTANT: Edit .env and add your Discord bot token!${NC}"
    else
        echo -e "${RED}✗ Failed to create .env file${NC}"
        exit 1
    fi
else
    echo -e "${GREEN}✓ .env file already exists${NC}"
fi

# Verify files
echo -e "${YELLOW}[5/5]${NC} Verifying installation..."
FILES_OK=true

if [ -f "main.py" ]; then
    echo -e "${GREEN}✓ main.py found${NC}"
else
    echo -e "${RED}✗ main.py not found${NC}"
    FILES_OK=false
fi

if [ -f "discord_bot.py" ]; then
    echo -e "${GREEN}✓ discord_bot.py found${NC}"
else
    echo -e "${RED}✗ discord_bot.py not found${NC}"
    FILES_OK=false
fi

if [ -f ".env" ]; then
    echo -e "${GREEN}✓ .env file found${NC}"
else
    echo -e "${RED}✗ .env file not found${NC}"
    FILES_OK=false
fi

echo ""
echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"

if [ "$FILES_OK" = true ]; then
    echo -e "${GREEN}✓ Setup complete!${NC}"
    echo ""
    echo -e "${YELLOW}Next steps:${NC}"
    echo "1. Edit .env and add your Discord bot token:"
    echo -e "   ${BLUE}nano .env${NC} or ${BLUE}vim .env${NC}"
    echo ""
    echo "2. Run the CLI version (Terminal):"
    echo -e "   ${BLUE}python3 main.py${NC}"
    echo ""
    echo "3. Or run the Discord bot:"
    echo -e "   ${BLUE}python3 discord_bot.py${NC}"
    echo ""
    echo "For help, see: QUICK_START.md or DISCORD_BOT_SETUP.md"
else
    echo -e "${RED}✗ Setup incomplete. Check the errors above.${NC}"
    exit 1
fi

echo -e "${BLUE}════════════════════════════════════════════════════════${NC}"
