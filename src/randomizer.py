import random
import os

from obs_websockets import OBSManager

class Randomizer:
    #Location of Weapon PNGS (This is also used for the names)
    WEAPONS_PATH = None

    #Handle Basic OBS Operations
    obs_manager = None

    #Sources and Scenes
    obs_scene = None
    weapon_image_source = None
    weapon_text_source = None

    #Weapons to use in Randomizer
    weapon_set = None

    #Weapon Subsets
    base_weapons = None
    variant_weapons = None
    clone_weapons = None

    #Weapon Set Randomizer Chooses From
    possible_weapons = None

    #Bools
    visibility = None

    def __init__(self, state):
        #Initilization
        try:
            self.obs_manager = OBSManager(state["Port"], state["Password"])
        except Exception as e:
            raise Exception("Could Not Connect To OBS")
        
        self.WEAPONS_PATH = state["Weapon Path"]

        self.obs_scene = state["Scene"]
        self.weapon_image_source = state["Image Source"]
        self.weapon_text_source = state["Text Source"]
         
        self.weapon_set = state["Weapon Set"] 
        print(os.path.abspath("."))
        self.load_weapons()  
        self.set_possible_weapons(state)
        self.visibility = True

    def disconnect(self):
        self.obs_manager.disconnect()

    def update_state(self, state):
        self.obs_scene = state["Scene"]
        self.weapon_image_source = state["Image Source"]
        self.weapon_text_source = state["Text Source"]
        self.weapon_set = state["Weapon Set"]

    def load_weapons(self):
        self.base_weapons = [os.path.splitext(x)[0] for x in os.listdir(self.WEAPONS_PATH + "/base")]
        self.variant_weapons = [os.path.splitext(x)[0] for x in os.listdir(self.WEAPONS_PATH + "/variants")]
        self.clone_weapons = [os.path.splitext(x)[0] for x in os.listdir(self.WEAPONS_PATH + "/clones")]

    def set_possible_weapons(self, state):
        set_name = state["Weapon Set"]
        if (set_name == "Base"):
            print("Using only original weapon versions")
            self.possible_weapons = self.base_weapons
        if (set_name == "Variants"):
            print("Using all weapon sets")
            self.possible_weapons = self.base_weapons + self.variant_weapons
        if (set_name == 'All'):
            print("Using all weapon including clones")
            self.possible_weapons = self.base_weapons + self.variant_weapons + self.clone_weapons

    def get_absolute_path(self, weapon):
        relative_path = self.WEAPONS_PATH

        if(weapon in self.base_weapons):
            relative_path += "/base/" + weapon
        if(weapon in self.variant_weapons):
            relative_path += "/variants/" + weapon
        if(weapon in self.clone_weapons):
            relative_path += "/clones/" + weapon

        relative_path += ".png"

        return os.path.abspath(relative_path)

    def get_random_weapon(self):
        if(self.set_possible_weapons == None or len(self.possible_weapons) <= 0):
            print("No Valid Weapons.")
            return False
        weapon = random.choice(self.possible_weapons)
        return weapon
    
    def set_weapon_obs(self, weapon):
        weapon_path = self.get_absolute_path(weapon)

        self.obs_manager.set_text(self.weapon_text_source, weapon)
        self.obs_manager.set_file(self.weapon_image_source, weapon_path)


    def toggle_visibility(self):
        if(self.visibility):
            self.obs_manager.set_source_visibility(self.obs_scene,self.weapon_image_source, False)
            self.obs_manager.set_source_visibility(self.obs_scene,self.weapon_text_source, False)
            self.visibility = False
        else:
            self.obs_manager.set_source_visibility(self.obs_scene,self.weapon_image_source, True)
            self.obs_manager.set_source_visibility(self.obs_scene,self.weapon_text_source, True)
            self.visibility = True