from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

import settings

app = FastAPI()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Equipment"]

class equipmentSchema(BaseModel):
    name: str
    iconId: str

def equipmentEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "name":item["name"],
        "iconId":item["iconId"]
    }

def equipmentsEntity(entity) -> list:
    return [equipmentEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

@app.get('/')
async def find_all_equipments():
    return serializeList(collection.find())

@app.post('/')
async def create_equipment(equipment: equipmentSchema):
    collection.insert_one(dict(equipment))
    return serializeList(collection.find())

@app.get('/{id}')
async def find_equipment(id):
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.put('/{id}')
async def update_equipment(id, equipment: equipmentSchema):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(equipment)})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.delete('/{id}')
async def delete_equipment(id: str):
    equipment = collection.find_one({"_id": ObjectId(id)})
    if equipment is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "Equipment not found"}
