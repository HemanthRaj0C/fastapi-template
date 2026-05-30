# FastAPI Backend Template (MongoDB)

FastAPI backend template with MongoDB integration.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start MongoDB (Docker)
docker run -d --name mongodb -p 27017:27017 mongo

# Start server
uvicorn main:app --reload --port 5000
```

## Available Routes

- `GET /api/health` - Health check endpoint (includes database connectivity status)

## Environment Variables

```
MONGODB_URI=mongodb://localhost:27017/myapp
```
