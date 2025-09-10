from fastapi import FastAPI, status, HTTPException
from datetime import datetime
from models import UserCreate, UserOut

app = FastAPI()

# In-memory "database" for demonstration
fake_db = []

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    """
    Create user with advanced validation.
    - Validation happens automatically before this function runs
    - Custom validators in UserCreate model enforce business rules
    """
    
    # If we reach here, validation passed!
    db_user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "join_date": datetime.now().isoformat(),
        "password": user_data.password,  # Will be filtered out by response_model
        "validation_status": "passed"
    }
    fake_db.append(db_user)
    
    return db_user

@app.get("/validation-rules/")
async def get_validation_rules():
    """Endpoint to show current validation rules."""
    return {
        "password_rules": {
            "min_length": 8,
            "requires_uppercase": True,
            "requires_lowercase": True,
            "requires_number": True,
            "requires_special_char": True
        },
        "username_rules": {
            "alphanumeric_only": True,
            "min_length": 3,
            "max_length": 20
        },
        "full_name_rules": {
            "allowed_characters": "letters, spaces, hyphens, apostrophes, periods",
            "min_length": 2,
            "max_length": 50,
            "optional": True
        }
    }

@app.get("/")
async def root():
    return {
        "message": "FastAPI Advanced Validation Demo",
        "endpoints": {
            "create_user": "POST /users/",
            "validation_rules": "GET /validation-rules/",
            "interactive_docs": "GET /docs"
        }
    }
