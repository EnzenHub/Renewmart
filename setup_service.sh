#!/bin/bash

# Setup script for RenewMart systemd service

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
    echo -e "${GREEN}[SUCCESS]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[WARNING]${NC} $1"
}

print_error() {
    echo -e "${RED}[ERROR]${NC} $1"
}

print_status "Setting up RenewMart as a systemd service..."

# Copy service file to systemd directory
print_status "Installing service file..."
sudo cp renewmart.service /etc/systemd/system/

# Reload systemd daemon
print_status "Reloading systemd daemon..."
sudo systemctl daemon-reload

# Enable the service
print_status "Enabling RenewMart service..."
sudo systemctl enable renewmart.service

print_success "Service installed and enabled!"

echo ""
print_status "Service Management Commands:"
echo "================================"
echo "Start service:    sudo systemctl start renewmart"
echo "Stop service:     sudo systemctl stop renewmart"
echo "Restart service:  sudo systemctl restart renewmart"
echo "Check status:     sudo systemctl status renewmart"
echo "View logs:        sudo journalctl -u renewmart -f"
echo "Disable service:  sudo systemctl disable renewmart"
echo ""
print_status "Manual Commands (without systemd):"
echo "========================================"
echo "Start services:   ./start_services.sh start"
echo "Stop services:    ./start_services.sh stop"
echo "Check status:     ./start_services.sh status"
echo "View logs:        ./start_services.sh logs"
echo ""

# Ask if user wants to start the service now
read -p "Do you want to start the service now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Starting RenewMart service..."
    sudo systemctl start renewmart
    sleep 3
    sudo systemctl status renewmart --no-pager
fi
