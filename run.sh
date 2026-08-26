#!/usr/bin/env bash
set -euo pipefail

SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
cd "$SCRIPT_DIR"

# ---------- helpers ----------
info()  { printf "\033[1;34m[INFO]\033[0m  %s\n" "$1"; }
error() { printf "\033[1;31m[ERROR]\033[0m %s\n" "$1"; exit 1; }

# ---------- pre-flight checks ----------
if [ ! -f ".env" ]; then
  error ".env file not found. Copy .env.example to .env and fill in your API keys."
fi

# Create / activate virtual environment
if [ ! -d "venv" ]; then
  info "Creating virtual environment..."
  python3 -m venv venv
fi

info "Activating virtual environment..."
source venv/bin/activate

# Install dependencies
info "Installing dependencies..."
pip install -q -r requirements.txt

# Ensure outputs directory exists
mkdir -p outputs

# ---------- run pipeline ----------
info "Running Artist Intelligence pipeline..."
python -m src.main

info "Pipeline complete. Check the outputs/ directory for results."
