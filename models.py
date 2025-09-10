from pydantic import BaseModel, EmailStr, field_validator
from typing import Optional
import re

class UserCreate(BaseModel):
    """
    Input model for user creation with advanced validation.
    Custom validators ensure data quality before processing.
    """
    username: str
    email: EmailStr
    password: str
    full_name: Optional[str] = None

    # Custom validator for password strength
    @field_validator('password')
    def password_must_be_strong(cls, v):
        """Validate password meets strength requirements."""
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters long')
        
        # Check for uppercase letters
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        
        # Check for lowercase letters
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        
        # Check for numbers
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        
        # Check for special characters
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        
        return v

    # Validator for username format
    @field_validator('username')
    def username_must_be_alphanumeric(cls, v):
        """Validate username contains only alphanumeric characters."""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric (letters and numbers only)')
        
        # Additional check: username length
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 20:
            raise ValueError('Username must be at most 20 characters long')
        
        return v

    # Validator for full_name (if provided)
    @field_validator('full_name')
    def full_name_must_be_proper_format(cls, v):
        """Validate full name format if provided."""
        if v is not None:
            # Check if it contains only letters, spaces, and common punctuation
            if not re.match(r'^[A-Za-z\s\-\'\.]+$', v):
                raise ValueError('Full name can only contain letters, spaces, hyphens, apostrophes, and periods')
            
            # Check length
            if len(v) < 2:
                raise ValueError('Full name must be at least 2 characters long')
            if len(v) > 50:
                raise ValueError('Full name must be at most 50 characters long')
        
        return v

class UserOut(BaseModel):
    """
    Output model for user responses.
    - Excludes password fields for security
    - Includes validation results
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    join_date: str
    validation_status: str = "passed"

    class Config:
        from_attributes = True
