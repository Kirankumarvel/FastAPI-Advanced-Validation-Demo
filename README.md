# FastAPI Advanced Validation Demo

A FastAPI application demonstrating advanced data validation using Pydantic's custom validators for robust input validation.

---

## 📋 Prerequisites

- Python 3.7 or higher
- pip (Python package manager)

---

## 🛠️ Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/Kirankumarvel/fastapi-advanced-validation-demo.git
   cd fastapi-advanced-validation-demo
   ```

2. **Create a virtual environment**
   ```bash
   python -m venv venv
   ```

3. **Activate the virtual environment**
   - **Windows:**
     ```bash
     venv\Scripts\activate
     ```
   - **macOS/Linux:**
     ```bash
     source venv/bin/activate
     ```

4. **Install dependencies with email support**
   ```bash
   pip install "pydantic[email]"
   pip install fastapi==0.104.1 uvicorn==0.24.0 pydantic==2.6.4 pydantic-extra-types==2.10.5
   ```

   **Or use requirements.txt:**
   ```bash
   pip install -r requirements.txt
   ```

---

## 📦 Dependencies

The project uses the following compatible versions:
- `fastapi==0.104.1` - The web framework for building APIs
- `uvicorn==0.24.0` - ASGI server for running FastAPI applications
- `pydantic==2.6.4` - Data validation with custom validators
- `pydantic-extra-types==2.10.5` - Additional validation types

**Important:** The `pydantic[email]` installation includes email validation support needed for `EmailStr` type.

---

## 🚀 Running the Application

1. **Start the development server**
   ```bash
   uvicorn main:app --reload --reload-exclude venv
   ```

2. **Access the application**
   - API: [http://127.0.0.1:8000](http://127.0.0.1:8000)
   - Interactive docs: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)
   - Alternative docs: [http://127.0.0.1:8000/redoc](http://127.0.0.1:8000/redoc)

---

## 📡 API Endpoints

### POST /users/
Create a new user with advanced validation rules.

**Request Body:**
```json
{
  "username": "johndoe123",
  "email": "john@example.com",
  "password": "SecurePass123!",
  "full_name": "John Doe"
}
```

**Response:**
```json
{
  "username": "johndoe123",
  "email": "john@example.com",
  "full_name": "John Doe",
  "join_date": "2023-12-07T10:30:00.000000"
}
```

---

## 🎯 Key Concept: Advanced Pydantic Validation

### Custom Field Validators
1. **Password Strength**: Minimum length and complexity requirements
2. **Username Format**: Alphanumeric characters only
3. **Automatic Error Messages**: Clear validation feedback
4. **Pre-Execution Validation**: Validation happens before your function runs

### Validation Rules
- **Password**: At least 8 characters, contains uppercase, lowercase, number, and special character
- **Username**: Alphanumeric characters only (a-z, A-Z, 0-9)
- **Email**: Valid email format (automatically validated by `EmailStr`)

---

## 🧪 Testing the API

### Test 1: Valid Request
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe123",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

### Test 2: Weak Password (Validation Error)
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "johndoe123",
    "email": "john@example.com",
    "password": "123",
    "full_name": "John Doe"
  }'
```

**Error Response:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "password"],
      "msg": "Password must be at least 8 characters long",
      "input": "123"
    }
  ]
}
```

### Test 3: Invalid Username (Validation Error)
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "username": "john_doe!",
    "email": "john@example.com",
    "password": "SecurePass123!",
    "full_name": "John Doe"
  }'
```

**Error Response:**
```json
{
  "detail": [
    {
      "type": "value_error",
      "loc": ["body", "username"],
      "msg": "Username must be alphanumeric",
      "input": "john_doe!"
    }
  ]
}
```

### Test 4: Missing Required Field
```bash
curl -X POST "http://127.0.0.1:8000/users/" \
  -H "Content-Type: application/json" \
  -d '{
    "email": "john@example.com",
    "password": "SecurePass123!"
  }'
```

---

## 📁 Project Structure

```
fastapi-advanced-validation-demo/
├── main.py          # Main application file
├── models.py        # Pydantic model with validators
├── requirements.txt # Project dependencies
├── README.md        # Project documentation
└── venv/            # Virtual environment (gitignored)
```

---

## 🔧 Code Explanation

### models.py
```python
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
        if not re.search(r'[A-Z]', v):
            raise ValueError('Password must contain at least one uppercase letter')
        if not re.search(r'[a-z]', v):
            raise ValueError('Password must contain at least one lowercase letter')
        if not re.search(r'[0-9]', v):
            raise ValueError('Password must contain at least one number')
        if not re.search(r'[!@#$%^&*(),.?":{}|<>]', v):
            raise ValueError('Password must contain at least one special character')
        return v

    # Validator for username format
    @field_validator('username')
    def username_must_be_alphanumeric(cls, v):
        """Validate username contains only alphanumeric characters."""
        if not v.isalnum():
            raise ValueError('Username must be alphanumeric')
        if len(v) < 3:
            raise ValueError('Username must be at least 3 characters long')
        if len(v) > 20:
            raise ValueError('Username must be at most 20 characters long')
        return v

class UserOut(BaseModel):
    """
    Output model for user responses.
    - Excludes password fields for security
    """
    username: str
    email: EmailStr
    full_name: Optional[str] = None
    join_date: str

    class Config:
        from_attributes = True
```

### main.py
```python
from fastapi import FastAPI, status
from datetime import datetime
from models import UserCreate, UserOut

app = FastAPI()

fake_db = []

@app.post("/users/", response_model=UserOut, status_code=status.HTTP_201_CREATED)
async def create_user(user_data: UserCreate):
    db_user = {
        "username": user_data.username,
        "email": user_data.email,
        "full_name": user_data.full_name,
        "join_date": datetime.now().isoformat(),
        "password": user_data.password
    }
    fake_db.append(db_user)
    return db_user

@app.get("/validation-rules/")
async def get_validation_rules():
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
        }
    }

@app.get("/")
async def root():
    return {"message": "FastAPI Advanced Validation Demo"}
```

---

## 🎓 Learning Points

### 1. **Custom Field Validators**
```python
@field_validator('password')
def password_must_be_strong(cls, v):
    if len(v) < 8:
        raise ValueError('Password must be at least 8 characters long')
    return v
```

### 2. **Multiple Validation Rules**
```python
# Password must have:
# - 8+ characters
# - Uppercase letter
# - Lowercase letter  
# - Number
# - Special character
```

### 3. **Automatic Error Handling**
- Validation happens before your function executes
- Clear, descriptive error messages
- Proper HTTP status codes (422 Unprocessable Entity)

### 4. **Business Logic in Models**
- Keep validation rules with data definitions
- Reusable across different endpoints
- Self-documenting validation requirements

---

## 🔧 Troubleshooting

### Common Issues:

1. **Validator import errors**
   ```bash
   # Ensure correct pydantic version
   pip install pydantic==2.6.4
   ```

2. **Regular expression issues**
   - Test regex patterns separately if having issues

3. **Validation too strict/lenient**
   - Adjust validation rules in models.py

4. **EmailStr import error**
   ```bash
   pip install "pydantic[email]"
   ```

---

## 📚 Learning Resources

- [Pydantic Validators](https://docs.pydantic.dev/concepts/validators/)
- [Field Validators](https://docs.pydantic.dev/concepts/validators/#field-validators)
- [FastAPI Request Validation](https://fastapi.tiangolo.com/tutorial/handling-errors/#override-the-default-exception-handlers)

---

## 🤝 Contributing

1. Fork the project
2. Create your feature branch (`git checkout -b feature/AmazingFeature`)
3. Commit your changes (`git commit -m 'Add some AmazingFeature'`)
4. Push to the branch (`git push origin feature/AmazingFeature`)
5. Open a Pull Request

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.

---

## 🙏 Acknowledgments

- Pydantic team for powerful validation capabilities
- FastAPI team for seamless integration
- Uvicorn team for the ASGI server
- Python community for ongoing support
