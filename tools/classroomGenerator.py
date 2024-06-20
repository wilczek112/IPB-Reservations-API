import json
import random

# List of school IDs
school_ids = ["ESTIG", "ESE", "ESA", "EsACT"]

# List of equipment
equipment = [
    {"_id": "6621677874e10184faac7f8c", "name": "Projector", "iconId": "projector_icon"},
    {"_id": "6621677874e10184faac7f8d", "name": "Whiteboard", "iconId": "whiteboard_icon"},
    {"_id": "6621677874e10184faac7f8e", "name": "Desk", "iconId": "desk_icon"},
    {"_id": "6621677874e10184faac7f8f", "name": "Chair", "iconId": "chair_icon"},
    {"_id": "662167ad74e10184faac954e", "name": "Computer", "iconId": "computer_icon"},
    {"_id": "662167ad74e10184faac954f", "name": "Bookshelf", "iconId": "bookshelf_icon"},
    {"_id": "662167ad74e10184faac9550", "name": "Microphone", "iconId": "microphone_icon"},
    {"_id": "662167ad74e10184faac9551", "name": "Table", "iconId": "table_icon"},
    {"_id": "662167ad74e10184faac9552", "name": "Laptop", "iconId": "laptop_icon"}
]

# Function to generate a classroom
def generate_classroom(existing_rooms):
    # Generate unique room number
    while True:
        floor = random.randint(1, 3)
        room_number = random.randint(1, 30)
        room = str(floor) + str(room_number).zfill(2)
        if room not in existing_rooms:
            existing_rooms.add(room)
            break

    # Generate school ID
    school_id = random.choice(school_ids)

    # Generate capacity
    capacity = random.randint(30, 70)

    # Generate equipment list
    num_equipment = random.randint(3, len(equipment))  # Generate a random number of equipment items, but not less than 3
    equipment_list = random.sample(equipment, k=num_equipment)
    equipment_ids = [item["_id"] for item in equipment_list]

    return {
        "Room": room,
        "Type": "Aula",
        "SchoolId": school_id,
        "Capacity": str(capacity),
        "EquipmentList": equipment_ids
    }

# Generate classrooms
existing_rooms = set()
classrooms = [generate_classroom(existing_rooms) for _ in range(30)]

# Wrap classrooms in a dictionary with the key "rooms"
classrooms_dict = {"rooms": classrooms}

# Print JSON
print(json.dumps(classrooms_dict, indent=4))
