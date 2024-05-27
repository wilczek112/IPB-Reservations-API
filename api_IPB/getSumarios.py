from pydantic import BaseModel
import requests

class ReservationSchema(BaseModel):
    aula: dict
    disciplinas: list
    docentes: list
    idAula: int
    sala: dict
    sumarios: list

def reservationEntity(item) -> dict:
    return {
        "aula": item["aula"],
        "disciplinas": item["disciplinas"],
        "docentes": item["docentes"],
        "idAula": item["idAula"],
        "sala": item["sala"],
        "sumarios": item["sumarios"],
        "inicio": item["aula"]["inicio"],
        "fim": item["aula"]["fim"]
    }

def reservationsEntity(entity) -> list:
    return [reservationEntity(item) for item in entity]

def get_reservations(codEscola: int, codSala: str):
    response = requests.get(f"https://api.example.com/event/{codEscola}/{codSala}")
    if response.status_code != 200:
        raise Exception("Reservations not found")
    data = response.json()
    return reservationsEntity(data)
