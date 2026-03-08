from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from bson import ObjectId
from dotenv import load_dotenv
from pydantic import BaseModel
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

class UserCreate(BaseModel):
    name: str
    email: str

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

def user_helper(user) -> dict:
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"]
    }

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

@app.get("/api/users", response_model=list[UserResponse])
async def get_users():
    db = get_db()
    users = await db.users.find().to_list(1000)
    return [user_helper(user) for user in users]

@app.get("/api/users/{user_id}", response_model=UserResponse)
async def get_user(user_id: str):
    db = get_db()
    user = await db.users.find_one({"_id": ObjectId(user_id)})
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user_helper(user)

@app.post("/api/users", response_model=UserResponse, status_code=201)
async def create_user(user: UserCreate):
    db = get_db()
    result = await db.users.insert_one(user.model_dump())
    new_user = await db.users.find_one({"_id": result.inserted_id})
    return user_helper(new_user)

@app.put("/api/users/{user_id}", response_model=UserResponse)
async def update_user(user_id: str, user: UserCreate):
    db = get_db()
    result = await db.users.update_one(
        {"_id": ObjectId(user_id)},
        {"$set": user.model_dump()}
    )
    if result.modified_count == 0:
        existing = await db.users.find_one({"_id": ObjectId(user_id)})
        if not existing:
            raise HTTPException(status_code=404, detail="User not found")
    updated_user = await db.users.find_one({"_id": ObjectId(user_id)})
    return user_helper(updated_user)

@app.delete("/api/users/{user_id}")
async def delete_user(user_id: str):
    db = get_db()
    result = await db.users.delete_one({"_id": ObjectId(user_id)})
    if result.deleted_count == 0:
        raise HTTPException(status_code=404, detail="User not found")
    return {"message": "User deleted successfully"}

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 5000))
    uvicorn.run(app, host="0.0.0.0", port=port)
