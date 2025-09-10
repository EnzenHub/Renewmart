#!/bin/bash

# RenewMart Services Startup Script
# This script starts both backend and frontend services

# Colors for output
RED='\033[0;31m'
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

# Function to print colored output
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
    
    while [ $port -le $((start_port + 100)) ]; do
        if ! check_port $port; then
            echo $port
            return 0
        fi
        port=$((port + 1))
    done
    
    print_error "No free ports found starting from $start_port"
    return 1
}

# Function to kill process on port
kill_port() {
    local port=$1
    local pid=$(lsof -ti:$port)
    if [ ! -z "$pid" ]; then
        print_warning "Killing process on port $port (PID: $pid)"
        kill -9 $pid
        sleep 2
    fi
}

# Function to start backend
start_backend() {
    print_status "Starting Backend Service..."
    
    # Find a free port for backend (starting from 8000)
    BACKEND_PORT=$(find_free_port 8000)
    if [ $? -ne 0 ]; then
        print_error "Failed to find a free port for backend"
        return 1
    fi
    
    print_status "Using port $BACKEND_PORT for backend service"
    
    # Navigate to backend directory
    cd /home/pradeep1a/RenewMart/Renewmart/backend
    
    # Check if virtual environment exists, if not create one
    if [ ! -d "venv" ]; then
        print_status "Creating virtual environment..."
        python3 -m venv venv
    fi
    
    # Activate virtual environment
    source venv/bin/activate
    
    # Install/update requirements
    print_status "Installing/updating Python dependencies..."
    pip install -r requirements.txt --break-system-packages
    
    # Start uvicorn server
    print_status "Starting uvicorn server on port $BACKEND_PORT..."
    nohup uvicorn app.main:app --reload --host 0.0.0.0 --port $BACKEND_PORT > ../logs/backend.log 2>&1 &
    BACKEND_PID=$!
    echo $BACKEND_PID > ../logs/backend.pid
    echo $BACKEND_PORT > ../logs/backend.port
    
    print_success "Backend started with PID: $BACKEND_PID on port $BACKEND_PORT"
    print_status "Backend logs: /home/pradeep1a/RenewMart/Renewmart/logs/backend.log"
}

# Function to start frontend
start_frontend() {
    print_status "Starting Frontend Service..."
    
    # Use port 3000 for frontend
    FRONTEND_PORT=3000
    if check_port $FRONTEND_PORT; then
        print_error "Port $FRONTEND_PORT is already in use"
        return 1
    fi
    
    print_status "Using port $FRONTEND_PORT for frontend service"
    
    # Navigate to frontend directory
    cd /home/pradeep1a/RenewMart/Renewmart/frontend
    
    # Check if node_modules exists, if not install dependencies
    if [ ! -d "node_modules" ]; then
        print_status "Installing Node.js dependencies..."
        npm install
    fi
    
    # Set PORT environment variable for React
    export PORT=$FRONTEND_PORT
    
    # Start React development server
    print_status "Starting React development server on port $FRONTEND_PORT..."
    nohup npm start > ../logs/frontend.log 2>&1 &
    FRONTEND_PID=$!
    echo $FRONTEND_PID > ../logs/frontend.pid
    echo $FRONTEND_PORT > ../logs/frontend.port
    
    print_success "Frontend started with PID: $FRONTEND_PID on port $FRONTEND_PORT"
    print_status "Frontend logs: /home/pradeep1a/RenewMart/Renewmart/logs/frontend.log"
}

# Function to stop services
stop_services() {
    print_status "Stopping all services..."
    
    # Stop backend
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/backend.pid" ]; then
        BACKEND_PID=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/backend.pid)
        if kill -0 $BACKEND_PID 2>/dev/null; then
            print_status "Stopping backend (PID: $BACKEND_PID)..."
            kill $BACKEND_PID
        fi
        rm -f /home/pradeep1a/RenewMart/Renewmart/logs/backend.pid
    fi
    
    # Stop frontend
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/frontend.pid" ]; then
        FRONTEND_PID=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/frontend.pid)
        if kill -0 $FRONTEND_PID 2>/dev/null; then
            print_status "Stopping frontend (PID: $FRONTEND_PID)..."
            kill $FRONTEND_PID
        fi
        rm -f /home/pradeep1a/RenewMart/Renewmart/logs/frontend.pid
    fi
    
    # Clean up port files
    rm -f /home/pradeep1a/RenewMart/Renewmart/logs/backend.port
    rm -f /home/pradeep1a/RenewMart/Renewmart/logs/frontend.port
    
    print_success "All services stopped"
}

# Function to show status
show_status() {
    print_status "Service Status:"
    echo "=================="
    
    # Check backend
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/backend.port" ]; then
        BACKEND_PORT=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/backend.port)
        if check_port $BACKEND_PORT; then
            print_success "Backend: Running on port $BACKEND_PORT"
        else
            print_error "Backend: Not running (expected port $BACKEND_PORT)"
        fi
    else
        print_error "Backend: Not running (no port file found)"
    fi
    
    # Check frontend
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/frontend.port" ]; then
        FRONTEND_PORT=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/frontend.port)
        if check_port $FRONTEND_PORT; then
            print_success "Frontend: Running on port $FRONTEND_PORT"
        else
            print_error "Frontend: Not running (expected port $FRONTEND_PORT)"
        fi
    else
        print_error "Frontend: Not running (no port file found)"
    fi
    
    echo ""
    print_status "Access URLs:"
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/backend.port" ]; then
        BACKEND_PORT=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/backend.port)
        SERVER_IP=$(hostname -I | awk '{print $1}')
        echo "Backend API: http://$SERVER_IP:$BACKEND_PORT"
        echo "API Docs: http://$SERVER_IP:$BACKEND_PORT/docs"
        echo "Local Backend: http://localhost:$BACKEND_PORT"
    fi
    if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/frontend.port" ]; then
        FRONTEND_PORT=$(cat /home/pradeep1a/RenewMart/Renewmart/logs/frontend.port)
        SERVER_IP=$(hostname -I | awk '{print $1}')
        echo "Frontend: http://$SERVER_IP:$FRONTEND_PORT"
        echo "Local Frontend: http://localhost:$FRONTEND_PORT"
    fi
}

# Function to show logs
show_logs() {
    local service=$1
    
    if [ "$service" = "backend" ] || [ "$service" = "all" ]; then
        print_status "Backend Logs:"
        echo "=============="
        if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/backend.log" ]; then
            tail -20 /home/pradeep1a/RenewMart/Renewmart/logs/backend.log
        else
            print_warning "Backend log file not found"
        fi
        echo ""
    fi
    
    if [ "$service" = "frontend" ] || [ "$service" = "all" ]; then
        print_status "Frontend Logs:"
        echo "==============="
        if [ -f "/home/pradeep1a/RenewMart/Renewmart/logs/frontend.log" ]; then
            tail -20 /home/pradeep1a/RenewMart/Renewmart/logs/frontend.log
        else
            print_warning "Frontend log file not found"
        fi
    fi
}

# Function to show network information
show_network_info() {
    print_status "Network Information:"
    echo "======================"
    
    # Get server IP
    SERVER_IP=$(hostname -I | awk '{print $1}')
    echo "Server IP: $SERVER_IP"
    
    # Get hostname
    HOSTNAME=$(hostname)
    echo "Hostname: $HOSTNAME"
    
    # Show all network interfaces
    echo ""
    print_status "Network Interfaces:"
    ip addr show | grep -E "inet [0-9]" | grep -v "127.0.0.1" | awk '{print "  " $2}' | cut -d'/' -f1
    
    echo ""
    print_status "Firewall Status:"
    if command -v ufw >/dev/null 2>&1; then
        ufw status | head -5
    else
        echo "UFW not installed or not available"
    fi
    
    echo ""
    print_status "Access Instructions:"
    echo "1. Make sure your firewall allows the ports"
    echo "2. If using cloud server, check security groups/firewall rules"
    echo "3. Access from other devices using: http://$SERVER_IP:PORT"
}

# Create logs directory if it doesn't exist
mkdir -p /home/pradeep1a/RenewMart/Renewmart/logs

# Main script logic
case "$1" in
    "start")
        print_status "Starting RenewMart Services..."
        start_backend
        sleep 3
        start_frontend
        sleep 2
        show_status
        ;;
    "stop")
        stop_services
        ;;
    "restart")
        stop_services
        sleep 2
        print_status "Restarting RenewMart Services..."
        start_backend
        sleep 3
        start_frontend
        sleep 2
        show_status
        ;;
    "status")
        show_status
        ;;
    "logs")
        show_logs ${2:-"all"}
        ;;
    "network")
        show_network_info
        ;;
    "backend")
        start_backend
        ;;
    "frontend")
        start_frontend
        ;;
    *)
        echo "Usage: $0 {start|stop|restart|status|logs|network|backend|frontend}"
        echo ""
        echo "Commands:"
        echo "  start     - Start both backend and frontend services"
        echo "  stop      - Stop all services"
        echo "  restart   - Restart all services"
        echo "  status    - Show status of all services"
        echo "  logs      - Show logs (usage: $0 logs [backend|frontend|all])"
        echo "  network   - Show network information and access instructions"
        echo "  backend   - Start only backend service"
        echo "  frontend  - Start only frontend service"
        echo ""
        echo "Examples:"
        echo "  $0 start                    # Start both services"
        echo "  $0 logs backend            # Show backend logs"
        echo "  $0 logs frontend           # Show frontend logs"
        echo "  $0 logs all                # Show all logs"
        echo "  $0 network                 # Show network info"
        exit 1
        ;;
esac
