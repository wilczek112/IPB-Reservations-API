from bson import ObjectId
from fastapi import FastAPI
from pydantic import BaseModel
from pymongo import MongoClient

import settings

app = FastAPI()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Reservation"]

class reservationSchema(BaseModel):
    StartTime: int
    EndTime: int
    RoomId: str
    ProfessorId: str
    Status: str
    SchoolId: str

def reservationEntity(item) -> dict:
    return {
        "id":str(item["_id"]),
        "StartTime":item["StartTime"],
        "EndTime":item["EndTime"],
        "RoomId":item["RoomId"],
        "ProfessorId": item["ProfessorId"],
        "Status": item["Status"],
        "SchoolId": item["SchoolId"]
    }

def reservationsEntity(entity) -> list:
    return [reservationEntity(item) for item in entity]

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

@app.get('/')
async def find_all_rezervations():
    return serializeList(collection.find())

@app.post('/')
async def create_reservation(reservation: reservationSchema):
    collection.insert_one(dict(reservation))
    return serializeList(collection.find())

@app.get('/{id}')
async def find_reservation(id):
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.put('/{id}')
async def update_reservation(id, reservation: reservationSchema):
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(reservation)})
    return serializeList(collection.find({"_id":ObjectId(id)}))

@app.delete('/{id}')
async def delete_reservation(id: str):
    reservation = collection.find_one({"_id": ObjectId(id)})
    if reservation is not None:
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "Reservation not found"}
