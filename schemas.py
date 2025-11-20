"""
Database Schemas for CTCHT Website

Each Pydantic model represents a MongoDB collection. The collection name is the
lowercased class name by convention (e.g., ContactMessage -> "contactmessage").
"""

from pydantic import BaseModel, Field, EmailStr
from typing import Optional

class ContactMessage(BaseModel):
    """Contact form submissions from the website."""
    first_name: str = Field(..., description="Sender first name")
    last_name: str = Field(..., description="Sender last name")
    email: EmailStr = Field(..., description="Sender email address")
    message: str = Field(..., description="Message body")
    phone: Optional[str] = Field(None, description="Optional phone number")

class NewsletterSubscriber(BaseModel):
    """Newsletter signups for The Beacon."""
    email: EmailStr = Field(..., description="Subscriber email address")
    first_name: Optional[str] = Field(None, description="Optional first name")
    last_name: Optional[str] = Field(None, description="Optional last name")

# Example schemas kept for reference (can be removed if not needed)
class User(BaseModel):
    name: str
    email: str
    address: str
    age: Optional[int] = None
    is_active: bool = True

class Product(BaseModel):
    title: str
    description: Optional[str] = None
    price: float
    category: str
    in_stock: bool = True
