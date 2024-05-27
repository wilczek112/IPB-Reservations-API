from pydantic import BaseModel
import requests

class SalaSchema(BaseModel):
    abrev: str
    abrevEscola: str
    codEscola: int
    codSala: str
    escola: str
    id: int
    ip: int
    nome: str

def salaEntity(item) -> dict:
    return {
        "abrev": item["abrev"],
        "abrevEscola": item["abrevEscola"],
        "codEscola": item["codEscola"],
        "codSala": item["codSala"],
        "escola": item["escola"],
        "id": item["id"],
        "ip": item["ip"],
        "nome": item["nome"]
    }

def salasEntity(entity) -> list:
    return [salaEntity(item) for item in entity]

def get_salas(codEscola: int):
    response = requests.get(f"https://api.example.com/event/salas/{codEscola}")
    if response.status_code != 200:
        raise Exception("Salas not found")
    data = response.json()
    return salasEntity(data)
