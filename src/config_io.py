import json

SAVESTATE_FILENAME = "config.json"

def save_state(state):
    with open(SAVESTATE_FILENAME, "w") as f:
        json.dump(state,f,indent=4)

def load_state():
    try:
        with open(SAVESTATE_FILENAME, "r") as f:
            state = json.load(f)
    except:
        state = {
            "Weapon Path": "splatoon-weapon-images",
            "Port": 4455,
            "Password": "Splatoon",
            "Scene": "SCENE",
            "Image Source": "WEAPON_IMAGE_SOURCE",
            "Text Source": "WEAPON_TEXT_SOURCE",
            "Weapon Set": "Variants"
        }
    return state