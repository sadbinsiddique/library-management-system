from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
from helpers.paths import USERS_FILE
from helpers.read_db import load_users
from helpers.write_db import write_records

app = FastAPI()

class UserModel(BaseModel):
    username: str | None = None
    full_name: str | None = None
    email: str | None = None

def load_user_db():
    users = load_users()
    return {user['id']: user for user in users}

user_db = load_user_db()

@app.get("/", response_model=dict, status_code=200, description="Get all users")
async def get_all_users():
    return user_db

@app.post("/", response_model=UserModel, status_code=201, description="Add a new user")
async def add_user(user: UserModel):
    if not all([user.username, user.full_name, user.email]):
        raise HTTPException(status_code=400, detail="Bad Request")

    for existing in user_db.values():
        if existing.get("username") == user.username:
            raise HTTPException(status_code=409, detail="Conflict")

    new_id = max(user_db.keys()) + 1 if user_db else 1
    user_db[new_id] = user.model_dump()

    rows = [f"{uid}|{u['username']}|{u['full_name']}|{u['email']}" for uid, u in user_db.items()]
    write_records(USERS_FILE, rows)

    return user_db[new_id]

@app.get("/{user_id}", response_model=UserModel, status_code=200, description="Get a user by ID")
async def get_user_by_id(user_id: int = Path(..., description="The ID of the user to retrieve")):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Not Found")
    return user_db[user_id]

@app.put("/{user_id}", response_model=UserModel, status_code=200, description="Update a user by ID")
async def update_user(user_id: int, user: UserModel):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Not Found")

    stored = user_db[user_id]
    stored["username"] = user.username or stored["username"]
    stored["full_name"] = user.full_name or stored["full_name"]
    stored["email"] = user.email or stored["email"]

    rows = [f"{uid}|{u['username']}|{u['full_name']}|{u['email']}" for uid, u in user_db.items()]
    write_records(USERS_FILE, rows)

    return stored

@app.delete("/{user_id}", status_code=204, description="Delete a user by ID")
async def delete_user(user_id: int):
    if user_id not in user_db:
        raise HTTPException(status_code=404, detail="Not Found")

    del user_db[user_id]

    rows = [f"{uid}|{u['username']}|{u['full_name']}|{u['email']}" for uid, u in user_db.items()]
    write_records(USERS_FILE, rows)

    return None