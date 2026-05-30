from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from dotenv import load_dotenv
import os

from config.database import get_db

load_dotenv()

app = FastAPI(title="FastAPI Backend with MongoDB")

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/api/health")
async def health_check():
    database = False
    try:
        db = get_db()
        await db.command("ping")
        database = True
    except Exception:
        pass
    return {
        "status": "ok",
        "message": "Backend is running!",
        "database": database
    }

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
