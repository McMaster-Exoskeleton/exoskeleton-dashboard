# Exoskeleton Telemetry Backend

FastAPI WebSocket server for streaming exoskeleton telemetry data.

## Requirements

- Python 3.9 or higher

## Setup

### 1. Create Virtual Environment

```bash
# macOS/Linux
python3 -m venv venv
source venv/bin/activate

# Windows
python -m venv venv
.\venv\Scripts\activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Run the Server

```bash
uvicorn app.main:app --reload
```

The server will start at `http://localhost:8000`

**Alternative port (if 8000 is in use):**
```bash
uvicorn app.main:app --reload --port 8080
```

## API Endpoints

### Health Check

```
GET /health
```

Returns server status:
```json
{
  "status": "healthy",
  "service": "exoskeleton-telemetry"
}
```

### WebSocket (Coming Soon)

```
WS /ws
```

Streams real-time telemetry data.

## Threshold Configuration

Alert thresholds can be overridden via environment variables:

- `THRESHOLDS_JSON`: JSON string with threshold values.
- `THRESHOLDS_PATH`: Path to a JSON file with threshold values.

Example JSON:
```json
{
  "motors": {
    "temperature": { "warning": 50, "critical": 60 },
    "current": { "warning": 10, "critical": 13 }
  },
  "ina228": {
    "voltage": { "warning": 27, "critical": 29 },
    "current": { "warning": 8, "critical": 12 }
  }
}
```

## Development

### Code Formatting

```bash
black app/
```

### Linting

```bash
ruff check app/
```

### Running Tests

```bash
pytest
```

## Project Structure

```
backend/
├── app/
│   ├── __init__.py
│   ├── main.py          # FastAPI application entry point
│   ├── models.py        # Pydantic data models (coming soon)
│   ├── data_collector.py # Mock data generator (coming soon)
│   └── websocket.py     # WebSocket endpoint (coming soon)
├── tests/               # Test files (coming soon)
├── requirements.txt     # Python dependencies
├── pyproject.toml       # Project configuration
└── README.md
```
