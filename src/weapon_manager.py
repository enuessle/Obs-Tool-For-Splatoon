#OLD VERSION, NOT RECOMENDED TO USE

import time
import os
import random
from obs_websockets import OBSManager

WEAPON_IMAGE_SOURCE = "*** Current Weapon Image"
WEAPON_TEXT_SOURCE = "*** Current Weapon Name"

WEAPONS_PATH = "splatoon-weapon-images"


# Sets OBS Sources to Show Picked Splatoon Weapon
class SplatWeaponManager:
    # Manage OBS States
    obs_manager = OBSManager("4455", "Splatoon")
    visibility = None

    # Different Weapon Subsets
    base_weapons = None
    variant_weapons = None
    clone_weapons = None

    # Selection of Weapons that can be picked
    valid_weapons = None

    def __init__(self):
        #Initilization
        print("Filling Up Splatoon Weapon Data..")
        self.base_weapons = [os.path.splitext(x)[0] for x in os.listdir(WEAPONS_PATH + "/base")]
        self.variant_weapons = [os.path.splitext(x)[0] for x in os.listdir(WEAPONS_PATH + "/variants")]
        self.clone_weapons = [os.path.splitext(x)[0] for x in os.listdir(WEAPONS_PATH + "/clones")]

        self.valid_weapons = self.set_valid()

        self.visibility = True

    # Sets what possible weapons can be used
    # "base", "variants", "all"
    def set_valid(self, set_name = "variants"):
        if (set_name == "base"):
            print("Using only original weapon versions")
            self.valid_weapons = self.base_weapons
        if (set_name == "variants"):
            print("Using all weapon sets")
            self.valid_weapons = self.base_weapons + self.variant_weapons
        if (set_name == 'all'):
            print("Using all weapon including clones")
            self.valid_weapons = self.base_weapons + self.variant_weapons + self.clone_weapons

    # Returns True if it selects a new random weapon. False Otherwise
    def get_random_weapon(self):
        if(len(self.valid_weapons) <= 0):
            print("No Valid Weapons.")
            return False
        self.set_weapon_obs(random.choice(self.valid_weapons))
        return True

    # Picks a Random Weapon, then removes it from Valid Weapons
    # Returns True if it selects a new random weapon. False Otherwise 
    def get_random_weapon_remove(self):
        if(len(self.valid_weapons) <= 0):
            print("No Weapons Left.")
            return False
        weapon = random.choice(self.valid_weapons)
        self.set_weapon_obs(weapon)
        self.valid_weapons.remove(weapon)
        return True




    def get_absolute_path(self, weapon):
        relative_path = WEAPONS_PATH

        if(weapon in self.base_weapons):
            relative_path += "/base/" + weapon
        if(weapon in self.variant_weapons):
            relative_path += "/variants/" + weapon
        if(weapon in self.clone_weapons):
            relative_path += "/clones/" + weapon

        relative_path += ".png"

        return os.path.abspath(relative_path)

    def set_weapon_obs(self, weapon):
        weapon_path = self.get_absolute_path(weapon)

        self.obs_manager.set_text(WEAPON_TEXT_SOURCE, "Current Weapon:\n" + weapon)
        self.obs_manager.set_file(WEAPON_IMAGE_SOURCE, weapon_path)


    def toggle_visibility(self, scene):
        if(self.visibility):
            self.obs_manager.set_source_visibility(scene,WEAPON_IMAGE_SOURCE, False)
            self.obs_manager.set_source_visibility(scene,WEAPON_TEXT_SOURCE, False)
            self.visibility = False
        else:
            self.obs_manager.set_source_visibility(scene,WEAPON_IMAGE_SOURCE, True)
            self.obs_manager.set_source_visibility(scene,WEAPON_TEXT_SOURCE, True)
            self.visibility = True
        


#Testing Code
if __name__ == '__main__':
    splat_weapon_manager = SplatWeaponManager()

    print("Printing Weapons Lists\n\n")
    print("Base Weapons\n")
    print(splat_weapon_manager.base_weapons)
    print("Variant Weapons\n")
    print(splat_weapon_manager.variant_weapons)
    print("Clone Weapons\n")
    print(splat_weapon_manager.clone_weapons)

    print("Valid Weapons All\n")
    splat_weapon_manager.set_valid("all")
    print(splat_weapon_manager.valid_weapons)

    print("Testing Random Weapon")
    splat_weapon_manager.get_random_weapon()
