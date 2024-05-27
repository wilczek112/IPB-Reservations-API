from bson import ObjectId
from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
import settings

router = APIRouter()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["User"]

class UserSchema(BaseModel):
    name: str
    surname: str
    role: str
    email: str
    password: str

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

@router.delete('/{id}')
async def delete_user(id: str):
    user = collection.find_one({"_id": ObjectId(id)})
    if user is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "User not found"}
