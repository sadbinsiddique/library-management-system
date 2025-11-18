# ============================================
# api_server.py
# ============================================

from fastapi import FastAPI, Query, HTTPException
from pydantic import BaseModel, EmailStr, field_validator
import math

app = FastAPI(
    title="Library Management System",
    description="An API service to demonstrate Library Management System API capabilities.",
    version="1.5.0"
)

# Static user database 
user_db = {
    1: {"name": "Alice", "age": 30, "phone": "+8801355598745", "date_of_birth": "1993-01-15", "email": "alice@example.com", "address": "123 Main St, City, State"},
    2: {"name": "Bob", "age": 25, "phone": "+8801954621874", "date_of_birth": "1998-05-20", "email": "bob@example.com", "address": "456 Oak Ave, Town, State"},
    3: {"name": "Charlie", "age": 35, "phone": "+8801921548798", "date_of_birth": "1988-09-10", "email": "charlie@example.com", "address": "789 Pine Rd, Village, State"},
    4: {"name": "Diana", "age": 28, "phone": "+880185551234", "date_of_birth": "1995-12-03", "email": "diana@example.com", "address": "321 Elm St, Borough, State"},
    5: {"name": "Edward", "age": 42, "phone": "+8801721548745", "date_of_birth": "1981-07-22", "email": "edward@example.com", "address": "654 Maple Dr, Township, State"},
    6: {"name": "Fiona", "age": 31, "phone": "+880188882229", "date_of_birth": "1992-03-18", "email": "fiona@example.com", "address": "987 Cedar Ln, Hamlet, State"},
    7: {"name": "George", "age": 29, "phone": "+880183337778", "date_of_birth": "1994-11-08", "email": "george@example.com", "address": "147 Birch Way, District, State"}
    }

# ---- 0) User Model ----
class UserModel(BaseModel):
    name: str
    age: int
    phone: str
    date_of_birth: str
    email: EmailStr
    address: str

    @field_validator('phone')
    @classmethod
    def validate_phone(cls, v):
        # Handle phone numbers with country code (+88)
        if v.startswith('+88'):
            # Remove country code and validate the remaining digits
            phone_digits = v[3:]  # Remove '+88'
            if not phone_digits.isdigit():
                raise ValueError('Phone number must contain only digits after country code')
            if len(phone_digits) != 11:
                raise ValueError('Phone number must be exactly 11 digits after country code')
            return v
        
        # Handle phone numbers without country code
        if not v.isdigit():
            raise ValueError('Phone number must contain only digits')
        if len(v) != 14:
            raise ValueError('Phone number must be exactly 11 digits')
        
        # Auto-add Bangladesh country code (+88) if phone starts with 01
        if v.startswith('01'):
            return f'+88{v}'
        
        return v

    @field_validator('age')
    @classmethod
    def validate_age(cls, v):
        if v <= 0:
            raise ValueError('Age must be greater than 0')
        if v > 150:
            raise ValueError('Age must be less than or equal to 150')
        return v

    class Config:
        schema_extra = {
            "example": {
                "name": "Henry",
                "age": 34,
                "phone": "+8801655598745",
                "date_of_birth": "1990-04-12",
                "email": "henry@example.com",
                "address": "321 Birch St, City, State"
            }
        }
        orm_mode = False

# ---- 1) GET: User ----
@app.get("/user")
def get_user_info(user_id: int = Query(..., description="ID of the user to retrieve", gt=0)):
    
    # Validate user_id
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail=f"User[{user_id}] not found")
    
    return user_db[user_id]


# ---- 2) POST: receive and return user data ----
@app.post("/user")
def create_user(user: UserModel):
    """
    Create a new user with the provided information and return the user details.
    """

    # Simulating saving to a database
    user_id = max(user_db.keys()) + 1 if user_db else 1
    user_db[user_id] = user.dict()
    return {"user_id": user_id, "user": user_db[user_id]}




# ---- 3) POST: receive and return dictionary ----
class DataModel(BaseModel):
    data: dict

@app.post("/process_dict1")
def process_dictionary_dict(payload: dict):
    return {"received_data": payload, "key_count": len(payload)}

@app.post("/process_dict2")
def process_dictionary_model(payload: DataModel):
    data = payload.data
    return {"received_data": data, "key_count": len(data)}

# Run using: uvicorn api_server:app --reload
