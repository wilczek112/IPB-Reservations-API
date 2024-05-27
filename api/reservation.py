from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from pymongo import MongoClient
from bson import ObjectId
from api_IPB import getSumarios

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

@router.get('/update/{codEscola}/{codSala}')
async def fetch_reservations_and_save_to_db(codEscola: int, codSala: str):
    try:
        reservations = getSumarios.get_reservations(codEscola, codSala)
    except Exception as e:
        raise HTTPException(status_code=404, detail=str(e))

    for reservation in reservations:
        new_reservation = {
            "StartTime": reservation["inicio"],
            "EndTime": reservation["fim"],
            "RoomId": reservation["sala"]["codSala"],
            "ProfessorId": reservation["docentes"][0]["login"] if reservation["docentes"] else None,
            "Status": "Active" if reservation["aula"]["activo"] else "Inactive",
            "SchoolId": reservation["sala"]["codEscola"]
        }
        collection.insert_one(new_reservation)

    return {"status": 200, "message": "Data fetched from API and saved to database successfully"}