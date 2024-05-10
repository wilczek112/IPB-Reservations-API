# main.py
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from api import reservation, room, equipment, user

app = FastAPI()

origins = ["*"]
# Configure CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.mount("/reservation", reservation.app)
app.mount("/room", room.app)
app.mount("/equipment", equipment.app)
app.mount("/user", user.app)
