# Exoskeleton Telemetry Dashboard

Real-time telemetry dashboard for monitoring exoskeleton performance, displaying joint positions, motor status, sensor data, power levels, and system health.

## Project Structure

```
exoskeleton-dashboard/
├── backend/         # Python FastAPI WebSocket server
├── frontend/        # React + TypeScript dashboard
├── docs/            # Documentation and specifications
├── scripts/         # Development and deployment scripts
└── README.md
```

## Quick Start

### Prerequisites

- **Python:** 3.9 or higher
- **Node.js:** 18 LTS or higher
- **npm:** 9 or higher (comes with Node.js)
- **Git:** For version control

### Platform-Specific Setup

#### macOS

```bash
# Install Homebrew (if not installed)
/bin/bash -c "$(curl -fsSL https://raw.githubusercontent.com/Homebrew/install/HEAD/install.sh)"

# Install Python and Node.js
brew install python@3.11 node@18

# Verify installations
python3 --version
node --version
npm --version
```

#### Linux (Ubuntu/Debian)

```bash
# Update package list
sudo apt update

# Install Python
sudo apt install python3 python3-pip python3-venv

# Install Node.js via NodeSource
curl -fsSL https://deb.nodesource.com/setup_18.x | sudo -E bash -
sudo apt install nodejs

# Verify installations
python3 --version
node --version
npm --version
```

#### Windows

1. **Python:** Download and install from [python.org](https://www.python.org/downloads/). Check "Add Python to PATH" during installation.
2. **Node.js:** Download and install the LTS version from [nodejs.org](https://nodejs.org/).
3. **Git:** Download and install from [git-scm.com](https://git-scm.com/download/win).

Open PowerShell or Git Bash and verify:
```powershell
python --version
node --version
npm --version
```

### Running the Application

#### Backend

```bash
cd backend

# Create virtual environment
python3 -m venv venv

# Activate virtual environment
# macOS/Linux:
source venv/bin/activate
# Windows:
.\venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run the server
uvicorn app.main:app --reload
```

The backend will be available at `http://localhost:8000`

#### Frontend

```bash
cd frontend

# Install dependencies
npm install

# Run development server
npm run dev
```

The frontend will be available at `http://localhost:5173`

## Technology Stack

### Backend
- Python 3.9+
- FastAPI
- Uvicorn (ASGI server)
- Pydantic (data validation)
- WebSockets

### Frontend
- React 18+
- TypeScript 5+
- Vite (build tool)
- Recharts or Chart.js (charts)

