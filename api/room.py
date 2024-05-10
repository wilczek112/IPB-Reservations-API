from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

import settings

app = FastAPI()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Room"]

class roomSchema(BaseModel):
    Room: str
    Type: str
    SchoolId: str
    Capacity: str
    EquipmentList: list

def roomEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "Room":item["Room"],
        "Type":item["Type"],
        "SchoolId":item["SchoolId"],
        "Capacity": item["Capacity"],
        "EquipmentList": item["EquipmentList"]
    }

def roomsEntity(entity) -> list:
    return [roomEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

@app.get('/')
async def find_all_rooms():
    return serializeList(collection.find())

@app.post('/')
async def create_room(room: roomSchema):
    collection.insert_one(dict(room))
    return serializeList(collection.find())

@app.get('/{id}')
async def find_room(id):
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.put('/{id}')
async def update_room(id, room: roomSchema):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(room)})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.delete('/{id}')
async def delete_room(id: str):
    room = collection.find_one({"_id": ObjectId(id)})
    if room is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "Room not found"}
