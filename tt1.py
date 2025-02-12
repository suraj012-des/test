from fastapi import FastAPI, HTTPException
from motor.motor_asyncio import AsyncIOMotorClient
from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional, Dict, Any
import json

# Initialize FastAPI app
app = FastAPI()

# MongoDB Connection
MONGO_URI = "mongodb+srv://vedita-admin:CESPH7G7bvpxeseE@cluster38164.07mrf.mongodb.net"
client = AsyncIOMotorClient(MONGO_URI)
db = client["vedita-ai-dev"]
collection = db["testsections"]

# Pydantic Models
class EstimatedTime(BaseModel):
    hours: int
    minutes: int

class TestSchema(BaseModel):
    testId: Optional[Dict[str, Any]] = None
    name: str
    description: str
    prompt: str
    order: int
    image: str
    videoLink: str
    estimatedTime: EstimatedTime
    questionsCount: int
    status: str
    created_at: Optional[datetime] = Field(default_factory=datetime.utcnow)
    updated_at: Optional[datetime] = Field(default_factory=datetime.utcnow)

@app.get("/")
async def root():
    return {"message": "API is running"}

@app.post("/add-test/")
async def add_test(test: TestSchema):
    try:
        test_dict = test.dict()
        test_dict["created_at"] = datetime.utcnow()
        test_dict["updated_at"] = datetime.utcnow()
        
        result = await collection.insert_one(test_dict)
        return {"message": "Test added successfully!", "id": str(result.inserted_id)}
    except Exception as e:
        print(f"Error: {str(e)}")  # Add logging
        raise HTTPException(status_code=500, detail=f"Error adding test: {str(e)}")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="127.0.0.1", port=8001)
