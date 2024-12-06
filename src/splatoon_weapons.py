#OLD VERSION, NOT RECOMMENDED TO USE


import keyboard
import time

from weapon_manager import SplatWeaponManager

SCENE = "Switch Gameplay"


weapon_manager = SplatWeaponManager()
weapon_manager.set_valid("variants")


print("Running Random Weapons\nPress F1 to Change Weapon Quickly. Press F2 To Change Slowly\nF3 To Toggle Visibility Of OBS Sources\nPress F4 To Random Weapon With No Repeats")
while True:
    if keyboard.read_key() == "f1":
        if(weapon_manager.get_random_weapon() == False):
            weapon_manager.toggle_visibility(SCENE)
    if keyboard.read_key() == "f2":
        if(weapon_manager.get_random_weapon() == False):
            weapon_manager.toggle_visibility(SCENE)
        time.sleep(0.5)
    if keyboard.read_key() == "f3":
        weapon_manager.toggle_visibility(SCENE)
        time.sleep(0.5)
    if keyboard.read_key() == "f4":
        if(weapon_manager.get_random_weapon_remove() == False):
            weapon_manager.toggle_visibility(SCENE)
        time.sleep(0.5)