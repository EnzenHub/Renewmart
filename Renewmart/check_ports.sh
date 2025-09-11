#!/bin/bash

# Port Checker Script for RenewMart
# This script checks which ports are available

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

print_status() {
    echo -e "${BLUE}[INFO]${NC} $1"
}

print_success() {
    echo -e "${GREEN}[FREE]${NC} $1"
}

print_error() {
    echo -e "${RED}[IN USE]${NC} $1"
}

# Function to check if a port is in use
check_port() {
    local port=$1
    if lsof -Pi :$port -sTCP:LISTEN -t >/dev/null 2>&1; then
        return 0  # Port is in use
    else
        return 1  # Port is free
    fi
}

# Function to find a free port starting from a given port
find_free_port() {
    local start_port=$1
    local port=$start_port
    
    while [ $port -le $((start_port + 10)) ]; do
        if ! check_port $port; then
            echo $port
            return 0
        fi
        port=$((port + 1))
    done
    
    echo "NONE"
    return 1
}

echo "=========================================="
echo "        RenewMart Port Checker"
echo "=========================================="
echo ""

print_status "Checking common development ports..."
echo ""

# Check backend ports (8000-8010)
echo "Backend Ports (8000-8010):"
echo "-------------------------"
for port in {8000..8010}; do
    if check_port $port; then
        print_error "Port $port"
    else
        print_success "Port $port"
    fi
done

echo ""

# Check frontend ports (3000-3010)
echo "Frontend Ports (3000-3010):"
echo "--------------------------"
for port in {3000..3010}; do
    if check_port $port; then
        print_error "Port $port"
    else
        print_success "Port $port"
    fi
done

echo ""

# Find recommended ports
echo "Recommended Ports:"
echo "-----------------"
BACKEND_FREE=$(find_free_port 8000)
FRONTEND_FREE=$(find_free_port 3000)

if [ "$BACKEND_FREE" != "NONE" ]; then
    print_success "Backend: Use port $BACKEND_FREE"
else
    print_error "Backend: No free ports found in range 8000-8010"
fi

if [ "$FRONTEND_FREE" != "NONE" ]; then
    print_success "Frontend: Use port $FRONTEND_FREE"
else
    print_error "Frontend: No free ports found in range 3000-3010"
fi

echo ""
echo "=========================================="
echo "Note: The start_services.sh script will"
echo "automatically find and use free ports!"
echo "=========================================="
