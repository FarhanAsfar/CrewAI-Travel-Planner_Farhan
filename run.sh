#!/bin/bash
# =============================================================================
# setup_and_run.sh
# AI Travel Planner — One-command setup and run script
#
# Usage:
#   chmod +x setup_and_run.sh   (only needed once)
#   ./setup_and_run.sh
# =============================================================================

set -e  # exit immediately if any command fails

# ── Colours for output ────────────────────────────────────────────────────────
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Colour

# ── Helpers ───────────────────────────────────────────────────────────────────
info()    { echo -e "${BLUE}[INFO]${NC}  $1"; }
success() { echo -e "${GREEN}[OK]${NC}    $1"; }
warn()    { echo -e "${YELLOW}[WARN]${NC}  $1"; }
error()   { echo -e "${RED}[ERROR]${NC} $1"; exit 1; }

# =============================================================================
echo ""
echo "================================================="
echo "   ✈️  AI Travel Planner — Setup & Run"
echo "================================================="
echo ""

# ── Step 1: Check we are at the project root ──────────────────────────────────
info "Checking project structure..."
if [ ! -f "pyproject.toml" ]; then
    error "pyproject.toml not found. Please run this script from the project root directory."
fi
success "Project root confirmed."

# ── Step 2: Check Python is installed ────────────────────────────────────────
info "Checking Python installation..."
if ! command -v python3 &> /dev/null; then
    error "Python3 is not installed. Please install Python 3.10 or higher."
fi
PYTHON_VERSION=$(python3 --version 2>&1 | awk '{print $2}')
success "Python $PYTHON_VERSION found."

# ── Step 3: Check CrewAI is installed ────────────────────────────────────────
info "Checking CrewAI installation..."
if ! command -v crewai &> /dev/null; then
    warn "CrewAI not found. Installing..."
    pip install crewai --quiet || error "Failed to install CrewAI."
    success "CrewAI installed."
else
    success "CrewAI found."
fi

# ── Step 4: Set up .env file ──────────────────────────────────────────────────
info "Checking .env file..."
if [ ! -f ".env" ]; then
    if [ -f ".env.example" ]; then
        cp .env.example .env
        warn ".env file not found — created from .env.example."
        echo ""
        echo -e "${YELLOW}  ⚠️  Please open .env and add your API keys:${NC}"
        echo "      GROQ_API_KEY    → https://console.groq.com"
        echo "      SERPER_API_KEY  → https://serper.dev"
        echo ""
        read -p "  Press Enter once you have added your API keys to .env..."
    else
        error ".env.example not found. Cannot create .env file."
    fi
else
    success ".env file found."
fi

# ── Step 5: Validate API keys are not placeholders ───────────────────────────
info "Validating API keys in .env..."

GROQ_KEY=$(grep "^GROQ_API_KEY=" .env | cut -d '=' -f2 | tr -d ' ')
SERPER_KEY=$(grep "^SERPER_API_KEY=" .env | cut -d '=' -f2 | tr -d ' ')

if [ -z "$GROQ_KEY" ] || [ "$GROQ_KEY" = "your_groq_api_key_here" ]; then
    error "GROQ_API_KEY is missing or not set in .env."
fi

if [ -z "$SERPER_KEY" ] || [ "$SERPER_KEY" = "your_serper_api_key_here" ]; then
    error "SERPER_API_KEY is missing or not set in .env."
fi

success "API keys found."

# ── Step 6: Install project dependencies ─────────────────────────────────────
info "Installing project dependencies via crewai install..."
crewai install || error "Dependency installation failed."
success "Dependencies installed."

# ── Step 7: Create output and logs directories ────────────────────────────────
info "Creating output and logs directories..."
mkdir -p logs output
success "Directories ready."

# ── Step 8: Run the project ───────────────────────────────────────────────────
echo ""
echo "================================================="
echo "   🚀  Launching AI Travel Planner..."
echo "================================================="
echo ""

crewai run || error "Failed to run the crew. Check logs/ for details."