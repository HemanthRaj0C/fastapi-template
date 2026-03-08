# FastAPI Backend Template

A minimal FastAPI backend template.

## Quick Start

```bash
# Create virtual environment
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Copy environment file
cp .env.example .env

# Start server
uvicorn main:app --reload --port 5000
```

## Available Routes

- `GET /api/health` - Health check endpoint

## Environment Variables

Copy `.env.example` to `.env` and configure as needed.
