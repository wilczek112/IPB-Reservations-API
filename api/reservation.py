from fastapi import APIRouter
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId

import settings

router = APIRouter()

client = MongoClient(settings.mongo_uri)
db = client["Space_reservation_database"]
collection = db["Reservation"]

class ReservationSchema(BaseModel):
    StartTime: int
    EndTime: int
    RoomId: str
    ProfessorId: str
    Status: str
    SchoolId: str

@router.get('/')
async def find_all_reservations():
    reservations = list(collection.find())
    for reservation in reservations:
        reservation["_id"] = str(reservation["_id"])
    return reservations

@router.post('/')
async def create_reservation(reservation: ReservationSchema):
    reservation = dict(reservation)
    result = collection.insert_one(reservation)
    return {"_id": str(result.inserted_id)}

@router.get('/{id}')
async def find_reservation(id: str):
    reservation = collection.find_one({"_id": ObjectId(id)})
    if reservation is not None:
        reservation["_id"] = str(reservation["_id"])
        return reservation
    else:
        return {"error": "Reservation not found"}

@router.put('/{id}')
async def update_reservation(id: str, reservation: ReservationSchema):
    reservation = dict(reservation)
    result = collection.update_one({"_id": ObjectId(id)}, {"$set": reservation})
    if result.modified_count > 0:
        return {"success": True}
    else:
        return {"error": "Reservation not found"}

@router.delete('/{id}')
async def delete_reservation(id: str):
    result = collection.delete_one({"_id": ObjectId(id)})
    if result.deleted_count > 0:
        return {"success": True}
    else:
        return {"error": "Reservation not found"}
