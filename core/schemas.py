from pydantic import BaseModel
from typing import Optional

# --- PRODUCT SCHEMAS ---
class ProductBase(BaseModel):
    name: str
    price: float
    description: Optional[str] = None

class ProductResponse(ProductBase):
    id: int
    class Config:
        from_attributes = True

# --- USER SCHEMAS (This was missing!) ---
class UserBase(BaseModel):
    username: str
    email: str

class UserCreate(UserBase):
    """Schema for creating a new user."""
    pass

class UserUpdate(BaseModel):
    """Schema for updating only the email."""
    email: str

class UserResponse(UserBase):
    """Schema for returning user data, including the ID."""
    id: int

    class Config:
        # This allows Pydantic to work with SQLAlchemy models
        from_attributes = True