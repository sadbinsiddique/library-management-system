# file: server/api_user_management.py
from fastapi import FastAPI, Query, Path, HTTPException
from pydantic import BaseModel
import os

app = FastAPI()

class UserModel(BaseModel):
    username: str
    full_name: str
    email: str

class UserUpdate(BaseModel):
    username: str = None
    full_name: str = None
    email: str = None

USERS_FILE = "database/users.txt"

def ensure_database_directory():
    os.makedirs("database", exist_ok=True)
    if not os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'w') as f:
            pass

def get_next_user_id():
    ensure_database_directory()
    max_id = 0
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    user_id = int(line.split('|')[0])
                    max_id = max(max_id, user_id)
    
    return max_id + 1

@app.get("/", response_model=dict, status_code=200)
async def get_all_users():
    ensure_database_directory()
    users = {}
    
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')
                    user_id = parts[0]
                    users[user_id] = {
                        "username": parts[1],
                        "full_name": parts[2],
                        "email": parts[3]
                    }
    
    return users

@app.post("/", response_model=dict, status_code=201)
async def add_user(user: UserModel):
    ensure_database_directory()
    
    # checking if username already exists
    if os.path.exists(USERS_FILE):
        with open(USERS_FILE, 'r') as f:
            for line in f:
                if line.strip():
                    parts = line.strip().split('|')

                    if parts[1] == user.username:
                        raise HTTPException(
                            status_code=409, 
                            detail="\n ------- Username already exists ------- \n"
                        )
    
    new_id = get_next_user_id()
    
    with open(USERS_FILE, 'a') as f:
        user_data = f"{new_id}|{user.username}|{user.full_name}|{user.email}\n"
        f.write(user_data)
    
    return {
        "id": new_id,
        "username": user.username,
        "full_name": user.full_name,
        "email": user.email
    }

@app.get("/{user_id}", response_model=dict, status_code=200)
async def get_user_by_id(user_id: int):
    ensure_database_directory()
    
    if not os.path.exists(USERS_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n ------ User not found ------ \n"
        )
    
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == user_id:
                    return {
                        "id": parts[0],
                        "username": parts[1],
                        "full_name": parts[2],
                        "email": parts[3]
                    }
    
    raise HTTPException(
        status_code=404, 
        detail="\n ------- User not found ------- \n"
    )

@app.put("/{user_id}", response_model=dict, status_code=200)
async def update_user(user_id: int, user_update: UserUpdate):
    ensure_database_directory()
    
    if not os.path.exists(USERS_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n ------- User not found ------- \n"
        )
    
    users = []
    user_found = False
    updated_user = None
    
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == user_id:
                    user_found = True
                    
                    # update only the provided fields
                    username = user_update.username if user_update.username else parts[1]
                    full_name = user_update.full_name if user_update.full_name else parts[2]
                    email = user_update.email if user_update.email else parts[3]
                    
                    updated_line = f"{parts[0]}|{username}|{full_name}|{email}\n"
                    users.append(updated_line)
                    
                    updated_user = {
                        "id": parts[0],
                        "username": username,
                        "full_name": full_name,
                        "email": email
                    }
                else:
                    users.append(line)
    
    if not user_found:
        raise HTTPException(
            status_code=404, 
            detail="\n ------- User not found ------- \n"
        )
    
    with open(USERS_FILE, 'w') as f:
        f.writelines(users)
    
    return updated_user

@app.delete("/{user_id}", status_code=204)
async def delete_user(user_id: int):
    ensure_database_directory()
    
    if not os.path.exists(USERS_FILE):
        raise HTTPException(
            status_code=404, 
            detail="\n ------- User not found ------- \n"
        )
    
    users = []
    user_found = False
    
    with open(USERS_FILE, 'r') as f:
        for line in f:
            if line.strip():
                parts = line.strip().split('|')
                if int(parts[0]) == user_id:
                    user_found = True
                else:
                    users.append(line)
    
    if not user_found:
        raise HTTPException(
            status_code=404, 
            detail="\n ------- User not found ------- \n"
        )
    
    with open(USERS_FILE, 'w') as f:
        f.writelines(users)
    
    return None