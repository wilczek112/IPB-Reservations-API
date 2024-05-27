from bson import ObjectId
from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from api_IPB import getSalas
import settings

router = APIRouter()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Room"]

class RoomSchema(BaseModel):
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

@router.get('/')
async def find_all_rooms():
    return serializeList(collection.find())

@router.post('/')
async def create_room(room: RoomSchema):
    collection.insert_one(dict(room))
    return serializeList(collection.find())

@router.get('/{id}')
async def find_room(id):
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.put('/{id}')
async def update_room(id, room: RoomSchema):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(room)})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.patch('/{id}')
async def cancel_room(id: str):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set": {"Status": "Cancelled"}})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_room(id: str):
    room = collection.find_one({"_id": ObjectId(id)})
    if room is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "Room not found"}

@router.get('/update/{codEscola}')
async def fetch_salas(codEscola: int):
    try:
        salas = getSalas.get_salas(codEscola)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    for sala in salas:
        room = {
            "Room": sala["codSala"],
            "Type": "Unknown",
            "SchoolId": sala["codEscola"],
            "Capacity": "Unknown",
            "EquipmentList": []
        }
        collection.insert_one(room)

    return {"status": 200, "message": "Data fetched from API and saved to database successfully"}