import dearpygui.dearpygui as dpg
from config_io import load_state, save_state
from randomizer import Randomizer

dpg.create_context()

State = load_state()
randomizer = None

def update_callback(sender, app_data):
    State[sender] = app_data

def set_console(text):
    dpg.set_value("Console", text)

def start_randomizer():
    global randomizer
    if(randomizer != None):
        set_console("Restarting Randomizer")
        randomizer.disconnect()
    else:
        set_console("Starting Randomizer")

    try:
        randomizer = Randomizer(State)
        set_console("Finished Starting Randomizer")
    except Exception as e:
        set_console("COULD NOT CONNECT TO OBS.\nDouble check OBS is open and that websockets server is enabled in OBS.")

def change_weapons(sender, app_data):
    State["Weapon Set"] = app_data
    if (randomizer == None):
        return
    randomizer.set_possible_weapons(State)
    set_console(f"New Weapon Set: {State["Weapon Set"]}")

def run_randomizer():
    if (randomizer == None):
        set_console("Randomizer Not Started Yet.")
        return
    weapon = randomizer.get_random_weapon()
    set_console(f"New Weapon is {weapon}")
    randomizer.set_weapon_obs(weapon)

def toggle_visibility():
     if (randomizer == None):
        set_console("Randomizer Not Started Yet.")
        return
     randomizer.toggle_visibility()

with dpg.window(tag="Primary Window"):
    dpg.add_text("Websocket Config")
    dpg.add_input_text(tag = "Port", label="Server Port", default_value= State["Port"], callback=update_callback)
    dpg.add_input_text(tag = "Password", label="Server Password", default_value= State["Password"], callback=update_callback)
    dpg.add_spacer(height=20)
    dpg.add_text("OBS Sources To Use")
    dpg.add_input_text(tag = "Scene", label="OBS Scene", default_value= State["Scene"], callback=update_callback)
    dpg.add_input_text(tag = "Image Source", label="Weapon Image Source", default_value= State["Image Source"], callback=update_callback)
    dpg.add_input_text(tag = "Text Source", label="Weapon Text Source", default_value= State["Text Source"], callback=update_callback)
    dpg.add_spacer(height=20)
    dpg.add_button(label="Start Randomizer", callback=start_randomizer)
    dpg.add_spacer(height=20)
    dpg.add_text("Weapon Sets")
    dpg.add_radio_button(tag = "Weapon Set", label = "Weapon Set",items=["Base","Variants","All"], default_value=State["Weapon Set"], callback=change_weapons)
    dpg.add_spacer(height=20)
    dpg.add_button(label="Toggle Visibility", callback=toggle_visibility)
    dpg.add_button(label="New Weapon", callback=run_randomizer)
    dpg.add_spacer(height=20)
    dpg.add_text("", tag = "Console")

dpg.create_viewport(title='Splatoon OBS Weapon Randomizer', width=600, height=600)
dpg.setup_dearpygui()
dpg.show_viewport()
dpg.set_primary_window("Primary Window", True)
try:
    dpg.start_dearpygui()
finally:
    save_state(State)
    dpg.destroy_context()