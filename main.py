from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import room, equipment, user, reservation  # Import reservation

app = FastAPI()

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(reservation.router, prefix="/reservation")
app.include_router(room.router, prefix="/room")
app.include_router(equipment.router, prefix="/equipment")
app.include_router(user.router, prefix="/user")
