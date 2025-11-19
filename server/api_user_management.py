from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel

app = FastAPI()

user_db = {
    1: {
        "username": "john_doe",
        "full_name": "John Doe",
        "email": "john.doe@example.com"
    },
    2: {
        "username": "jane_smith",
        "full_name": "Jane Smith",
        "email": "jane.smith@example.com"
    },
    3: {
        "username": "alice_wong",
        "full_name": "Alice Wong",
        "email": "alice.wong@example.com"
    },
    4: {
        "username": "bob_jackson",
        "full_name": "Bob Jackson",
        "email": "bob.jackson@example.com"
    },
    5: {
        "username": "carla_martin",
        "full_name": "Carla Martin",
        "email": "carla.martin@example.com"
    },
    6: {
        "username": "daniel_lee",
        "full_name": "Daniel Lee",
        "email": "daniel.lee@example.com"
    },
    7: {
        "username": "emma_green",
        "full_name": "Emma Green",
        "email": "emma.green@example.com"
    },
    8: {
        "username": "frank_hill",
        "full_name": "Frank Hill",
        "email": "frank.hill@example.com"
    },
    9: {
        "username": "grace_kim",
        "full_name": "Grace Kim",
        "email": "grace.kim@example.com"
    },
    10: {
        "username": "henry_clark",
        "full_name": "Henry Clark",
        "email": "henry.clark@example.com"
    }
}

class UserModel(BaseModel):
    username: str
    full_name: str
    email: str

@app.get("/", response_model=dict, status_code=200)
async def get_all_users():
    return {"users": user_db}

@app.post("/", response_model=UserModel, status_code=201)
async def add_user(user: UserModel):
    for existing in user_db.values():
        if existing.get("email") == user.email:
            raise HTTPException(status_code=400, detail="Email already exists")
    new_id = max(user_db.keys()) + 1 if user_db else 1
    user_data = user.model_dump()
    user_db[new_id] = user_data
    return user_db[new_id]

@app.get("/{user_id}", response_model=UserModel, status_code=200)
async def get_user_by_id(
    user_id: int = Path(..., description="The ID of the user to retrieve")
):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    return user_db[user_id]

@app.put("/{user_id}", response_model=UserModel, status_code=200)
async def update_user(
    user: UserModel, user_id: int = Path(..., description="The ID of the user to update")
):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    user_db[user_id] = user.model_dump()
    return user_db[user_id]

@app.delete("/{user_id}", response_model=UserModel, status_code=200)
async def delete_user(
    user_id: int = Path(..., description="The ID of the user to delete")
):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="User not found")
    deleted_user = user_db.pop(user_id)
    return deleted_user