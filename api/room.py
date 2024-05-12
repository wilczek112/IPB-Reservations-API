from bson import ObjectId
from fastapi import FastAPI, APIRouter
from pydantic import BaseModel
from pymongo import MongoClient

import settings

router = APIRouter()  # Change app to router

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Reservation"]  # Change collection to Reservation

class ReservationSchema(BaseModel):  # Change roomSchema to ReservationSchema
    StartTime: int
    EndTime: int
    RoomId: str
    ProfessorId: str
    Status: str
    SchoolId: str

def reservationEntity(item) -> dict:  # Change roomEntity to reservationEntity
    return {
        "id":str(item["_id"]),
        "StartTime":item["StartTime"],
        "EndTime":item["EndTime"],
        "RoomId":item["RoomId"],
        "ProfessorId": item["ProfessorId"],
        "Status": item["Status"],
        "SchoolId": item["SchoolId"]
    }

def reservationsEntity(entity) -> list:  # Change roomsEntity to reservationsEntity
    return [reservationEntity(item) for item in entity]  # Change roomEntity to reservationEntity

def serializeDict(a) -> dict:
    return {**{i:str(a[i]) for i in a if i=='_id'},**{i:a[i] for i in a if i!='_id'}}

def serializeList(entity) -> list:
    return [serializeDict(a) for a in entity]

@router.get('/')
async def find_all_reservations():  # Change find_all_rooms to find_all_reservations
    return serializeList(collection.find())

@router.post('/')
async def create_reservation(reservation: ReservationSchema):  # Change create_room to create_reservation and room to reservation
    collection.insert_one(dict(reservation))  # Change room to reservation
    return serializeList(collection.find())

@router.get('/{id}')
async def find_reservation(id):  # Change find_room to find_reservation
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.put('/{id}')
async def update_reservation(id, reservation: ReservationSchema):  # Change update_room to update_reservation and room to reservation
    collection.find_one_and_update({"_id":ObjectId(id)}, {"$set":dict(reservation)})  # Change room to reservation
    return serializeList(collection.find({"_id":ObjectId(id)}))

@router.delete('/{id}')
async def delete_reservation(id: str):  # Change delete_room to delete_reservation
    reservation = collection.find_one({"_id": ObjectId(id)})  # Change room to reservation
    if reservation is not None:  # Change room to reservation
        collection.delete_one({"_id": ObjectId(id)})
        return {"status": 200, "message": "Successfully deleted"}
    else:
        return {"status": 404, "message": "Reservation not found"}  # Change Room not found to Reservation not found
