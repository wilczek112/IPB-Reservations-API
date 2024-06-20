from bson import ObjectId
from fastapi import APIRouter, Depends, HTTPException, status
from typing import Optional
from pydantic import BaseModel
from pymongo import MongoClient
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jose import jwt, JWTError
from datetime import datetime, timedelta

import settings

router = APIRouter()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["User"]

SECRET_KEY = "J****PIS*BoToK****takjestHeHe"  # Replace with your secret key
ALGORITHM = "HS256"
ACCESS_TOKEN_EXPIRE_MINUTES = 1440

class UserSchema(BaseModel):
    name: str
    surname: str
    role: str
    email: str
    password: str

class ChangePasswordSchema(BaseModel):
    old_password: str
    new_password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/token")

def userEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "surname":item["surname"],
        "role": item["role"],
        "email": item["email"],
        "password": item["password"]
    }

def usersEntity(entity) -> list:
    return [userEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt

def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_data = TokenData(email=email)
    except JWTError:
        raise credentials_exception
    user = collection.find_one({"email": token_data.email})
    if user is None:
        raise credentials_exception
    return user["email"]

@router.get("/check-token")
async def check_token(current_user: str = Depends(get_current_user)):
    return {"status": 200, "message": "Token is valid"}

@router.get('/')
async def find_all_users():
    return serializeList(collection.find())

@router.post('/')
async def create_user(user: UserSchema):
    collection.insert_one(dict(user))
    return serializeList(collection.find())

@router.get('/{id}')
async def find_user(id):
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.put('/{id}')
async def update_user(id, user: UserSchema):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(user)})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.get('/email/{email}')
async def find_user_by_email(email: str):
    user = collection.find_one({"email": email})
    if user is not None:
        return serializeDict(user)
    else:
        return {"status": 404, "message": "User not found"}

@router.patch('/cph/{email}')
async def change_password(email: str, password_data: ChangePasswordSchema):
    user = collection.find_one({"email": email})
    if user is not None:
        if user['password'] == password_data.old_password:
            collection.find_one_and_update(
                {"email": email},
                {"$set": {"password": password_data.new_password}}
            )
            return {"status": 200, "message": "Password successfully updated"}
        else:
            return {"status": 400, "message": "Old password does not match"}
    else:
        raise HTTPException(status_code=404, detail=f"User with email {email} not found. Received data: {password_data}")
@router.delete('/{id}')
async def delete_user(id: str):
    user = collection.find_one({"_id": ObjectId(id)})
    if user is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "User not found"}

@router.post("/token", response_model=Token)
def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends()):
    email = form_data.username  # Here username is actually the user's email

    # You might want to check if a user with this email exists in your database
    user = collection.find_one({"email": email})
    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="User not found",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user["email"]}, expires_delta=access_token_expires
    )
    return {"access_token": access_token, "token_type": "bearer"}