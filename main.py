import os
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, EmailStr
from bson import ObjectId

from database import db, create_document, get_documents
from schemas import ContactMessage, NewsletterSubscriber

app = FastAPI(title="CTCHT API")

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ObjectIdStr(str):
    @classmethod
    def __get_validators__(cls):
        yield cls.validate

    @classmethod
    def validate(cls, v):
        if isinstance(v, ObjectId):
            return str(v)
        if isinstance(v, str):
            try:
                ObjectId(v)
                return v
            except Exception:
                raise ValueError("Invalid ObjectId string")
        raise ValueError("Not a valid ObjectId")

class ContactResponse(BaseModel):
    id: ObjectIdStr

class SubscriberResponse(BaseModel):
    id: ObjectIdStr

@app.get("/")
def read_root():
    return {"message": "CTCHT API is running"}

@app.get("/test")
def test_database():
    """Verify DB connectivity and list collections."""
    response = {
        "backend": "✅ Running",
        "database": "❌ Not Available",
        "database_url": "❌ Not Set",
        "database_name": "❌ Not Set",
        "connection_status": "Not Connected",
        "collections": []
    }
    try:
        if db is not None:
            response["database"] = "✅ Available"
            response["database_url"] = "✅ Set" if os.getenv("DATABASE_URL") else "❌ Not Set"
            response["database_name"] = os.getenv("DATABASE_NAME") or "❌ Not Set"
            try:
                collections = db.list_collection_names()
                response["collections"] = collections[:10]
                response["connection_status"] = "Connected"
                response["database"] = "✅ Connected & Working"
            except Exception as e:
                response["database"] = f"⚠️ Connected but Error: {str(e)[:80]}"
        else:
            response["database"] = "⚠️ Available but not initialized"
    except Exception as e:
        response["database"] = f"❌ Error: {str(e)[:80]}"
    return response

@app.post("/contact", response_model=ContactResponse)
def submit_contact(payload: ContactMessage):
    """Store a contact message from the website."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    new_id = create_document("contactmessage", payload)
    return {"id": new_id}

@app.post("/newsletter/subscribe", response_model=SubscriberResponse)
def subscribe_newsletter(payload: NewsletterSubscriber):
    """Store a newsletter subscription."""
    if db is None:
        raise HTTPException(status_code=500, detail="Database not configured")
    # Allow duplicates to keep simple; dedupe can be added later
    new_id = create_document("newslettersubscriber", payload)
    return {"id": new_id}

# Simple public content endpoints (static for now, could be made dynamic later)
class Event(BaseModel):
    title: str
    date: str
    location: str
    description: str

@app.get("/events", response_model=List[Event])
def list_events():
    return [
        Event(title="Meet Us in the Garden", date="Every Friday", location="Uptown Campus Garden", description="Urban gardening and community building."),
        Event(title="Crafts and Conversations", date="Monthly", location="Clifton Court Hall", description="Relaxing craft activities and dialogue."),
    ]

if __name__ == "__main__":
    import uvicorn
    port = int(os.getenv("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
