#!/bin/bash

# Firewall Setup Script for RenewMart
# This script configures UFW firewall to allow access to your services

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

echo "=========================================="
echo "        RenewMart Firewall Setup"
echo "=========================================="
echo ""

# Check if UFW is installed
if ! command -v ufw >/dev/null 2>&1; then
    print_error "UFW (Uncomplicated Firewall) is not installed!"
    print_status "Installing UFW..."
    sudo apt update && sudo apt install ufw -y
    if [ $? -ne 0 ]; then
        print_error "Failed to install UFW"
        exit 1
    fi
fi

print_status "Current UFW status:"
sudo ufw status

echo ""
print_status "Setting up firewall rules for RenewMart..."

# Allow SSH (important!)
print_status "Allowing SSH access..."
sudo ufw allow ssh

# Allow HTTP and HTTPS
print_status "Allowing HTTP (80) and HTTPS (443)..."
sudo ufw allow 80
sudo ufw allow 443

# Allow development ports (3000-3010 for frontend, 8000-8010 for backend)
print_status "Allowing development ports..."
sudo ufw allow 3000:3010/tcp
sudo ufw allow 8000:8010/tcp

# Allow PostgreSQL (if needed for external access)
print_status "Allowing PostgreSQL (5432)..."
sudo ufw allow 5432

echo ""
print_status "Firewall rules added. Current status:"
sudo ufw status numbered

echo ""
print_warning "IMPORTANT: Before enabling UFW, make sure SSH is allowed!"
read -p "Do you want to enable UFW now? (y/n): " -n 1 -r
echo
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Enabling UFW firewall..."
    sudo ufw --force enable
    print_success "UFW firewall enabled!"
else
    print_warning "UFW not enabled. You can enable it later with: sudo ufw enable"
fi

echo ""
print_status "Firewall Configuration Summary:"
echo "=================================="
echo "✅ SSH (22) - Remote access"
echo "✅ HTTP (80) - Web traffic"
echo "✅ HTTPS (443) - Secure web traffic"
echo "✅ Frontend ports (3000-3010) - React development"
echo "✅ Backend ports (8000-8010) - FastAPI development"
echo "✅ PostgreSQL (5432) - Database access"
echo ""
print_status "Your RenewMart services should now be accessible from other devices!"
echo ""
print_status "To check firewall status anytime: sudo ufw status"
print_status "To disable firewall: sudo ufw disable"
print_status "To reset firewall: sudo ufw --force reset"
