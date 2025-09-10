# 🚀 RenewMart Server Management Guide

This guide explains how to control, monitor, and manage your RenewMart application on the server.

## 📁 **Available Management Files**

| File | Purpose | Usage |
|------|---------|-------|
| `start_services.sh` | Main control script for starting/stopping services | Daily management |
| `setup_service.sh` | Install system service for 24/7 operation | One-time setup |
| `renewmart.service` | System service configuration file | Auto-generated |
| `setup_firewall.sh` | Configure firewall rules | One-time setup |
| `check_ports.sh` | Check available ports | Troubleshooting |

## 🎯 **Quick Start Commands**

### **Start Your Application**
```bash
./start_services.sh start
```

### **Stop Your Application**
```bash
./start_services.sh stop
```

### **Check Status**
```bash
./start_services.sh status
```

### **View Logs**
```bash
./start_services.sh logs
```

## 🔧 **Detailed Management Commands**

### **1. Manual Service Control (Development/Testing)**

#### **Start Services**
```bash
# Start both backend and frontend
./start_services.sh start

# Start only backend
./start_services.sh backend

# Start only frontend
./start_services.sh frontend
```

#### **Stop Services**
```bash
# Stop all services
./start_services.sh stop
```

#### **Restart Services**
```bash
# Restart all services
./start_services.sh restart
```

#### **Monitor Services**
```bash
# Check service status
./start_services.sh status

# View all logs
./start_services.sh logs

# View backend logs only
./start_services.sh logs backend

# View frontend logs only
./start_services.sh logs frontend

# Show network information
./start_services.sh network
```

### **2. System Service Control (Production/24-7)**

#### **First Time Setup**
```bash
# Install as system service (run once)
./setup_service.sh
```

#### **Service Management**
```bash
# Start the service
sudo systemctl start renewmart

# Stop the service
sudo systemctl stop renewmart

# Restart the service
sudo systemctl restart renewmart

# Check service status
sudo systemctl status renewmart

# Enable auto-start on boot
sudo systemctl enable renewmart

# Disable auto-start on boot
sudo systemctl disable renewmart
```

#### **View Service Logs**
```bash
# View real-time logs
sudo journalctl -u renewmart -f

# View recent logs
sudo journalctl -u renewmart --since "1 hour ago"

# View all logs
sudo journalctl -u renewmart
```

## 🌐 **Access URLs**

### **External Access (from any device)**
- **Frontend**: http://149.102.158.71:PORT
- **Backend API**: http://149.102.158.71:PORT
- **API Documentation**: http://149.102.158.71:PORT/docs

### **Local Access (from server)**
- **Frontend**: http://localhost:PORT
- **Backend**: http://localhost:PORT

*Note: PORT numbers are automatically assigned and displayed when you run `./start_services.sh status`*

## 🛠️ **Troubleshooting Commands**

### **Check What's Running**
```bash
# Check service status
./start_services.sh status

# Check specific ports
lsof -i :8000
lsof -i :3000
lsof -i :8001
lsof -i :3001

# Check all listening ports
netstat -tulpn | grep LISTEN
```

### **Check Available Ports**
```bash
# Run port checker
./check_ports.sh
```

### **Emergency Stop (Kill Everything)**
```bash
# Kill all processes on specific ports
sudo lsof -ti:8000 | xargs kill -9
sudo lsof -ti:8001 | xargs kill -9
sudo lsof -ti:8002 | xargs kill -9
sudo lsof -ti:3000 | xargs kill -9
sudo lsof -ti:3001 | xargs kill -9
sudo lsof -ti:3010 | xargs kill -9

# Kill all uvicorn processes
sudo pkill -f uvicorn

# Kill all node processes
sudo pkill -f node

# Kill all React processes
sudo pkill -f react-scripts
```

### **Check Firewall Status**
```bash
# Check UFW status
sudo ufw status

# Check if specific port is allowed
sudo ufw status | grep 8000
sudo ufw status | grep 3000
```

### **Check Database Connection**
```bash
# Test PostgreSQL connection
sudo -u postgres psql -c "SELECT version();"

# Test database connection
psql -h localhost -U postgres -d renewmart_db -c "SELECT 1;"
```

## 📊 **Service Status Indicators**

### **Manual Services**
- ✅ `[SUCCESS] Backend: Running on port XXXX`
- ✅ `[SUCCESS] Frontend: Running on port XXXX`
- ❌ `[ERROR] Backend: Not running`
- ❌ `[ERROR] Frontend: Not running`

### **System Service**
- ✅ `Active: active (running)`
- ❌ `Active: inactive (dead)`
- ⚠️ `Active: failed`

## 🔄 **Workflow Examples**

### **Daily Development Workflow**
```bash
# 1. Start services
./start_services.sh start

# 2. Check status
./start_services.sh status

# 3. View logs if needed
./start_services.sh logs

# 4. Stop when done
./start_services.sh stop
```

### **Production Deployment Workflow**
```bash
# 1. First time setup
./setup_service.sh

# 2. Start service
sudo systemctl start renewmart

# 3. Enable auto-start
sudo systemctl enable renewmart

# 4. Check status
sudo systemctl status renewmart

# 5. Monitor logs
sudo journalctl -u renewmart -f
```

### **Troubleshooting Workflow**
```bash
# 1. Check status
./start_services.sh status

# 2. Check logs
./start_services.sh logs

# 3. Check ports
./check_ports.sh

# 4. Check firewall
sudo ufw status

# 5. Restart if needed
./start_services.sh restart
```

## 🚨 **Emergency Procedures**

### **If Services Won't Start**
```bash
# 1. Check logs
./start_services.sh logs

# 2. Check ports
./check_ports.sh

# 3. Kill conflicting processes
sudo pkill -f uvicorn
sudo pkill -f node

# 4. Restart
./start_services.sh restart
```

### **If External Access Fails**
```bash
# 1. Check firewall
sudo ufw status

# 2. Add missing ports
sudo ufw allow 8000/tcp
sudo ufw allow 3000/tcp

# 3. Check service status
./start_services.sh status
```

### **If Database Connection Fails**
```bash
# 1. Check PostgreSQL status
sudo systemctl status postgresql

# 2. Check database credentials in .env file
cat backend/.env

# 3. Test database connection
psql -h localhost -U postgres -d renewmart_db
```

## 📝 **Important Notes**

- **Ports are automatically assigned** - the system finds free ports automatically
- **Logs are stored** in the `logs/` directory
- **Firewall rules** need to be configured for external access
- **Database credentials** are in `backend/.env` file
- **System service** runs 24/7 and auto-restarts on failure
- **Manual services** stop when you disconnect from the server

## 🆘 **Getting Help**

If you encounter issues:

1. **Check the logs**: `./start_services.sh logs`
2. **Check the status**: `./start_services.sh status`
3. **Check available ports**: `./check_ports.sh`
4. **Check firewall**: `sudo ufw status`
5. **Restart services**: `./start_services.sh restart`

---

**Last Updated**: September 2025  
**Server IP**: 149.102.158.71  
**Application**: RenewMart
