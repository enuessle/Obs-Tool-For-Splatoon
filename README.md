# Splat-OBS
Splatoon Weapon Randomizer For OBS. Runs Through Python

## What it Does
OBSWebsocket handle sources

## Requirements
Have OBS v28 or higher

Have Python

If it needs missing moduales, pip install them

## Basic How To
Go to OBS, Tools, WebSocket Server Settings

Enable WebSocket server

Use same Server Port and Password as websockets_auth.py (you can change these but I recommend keeping Port as 4455)

In `splatoon_weapons.py`, change "SCENE" to the name of the obs scene you want this on

In `weapon_manager.py`, make sure `WEAPON_IMAGE_SOURCE` is the name of an image source in OBS

In `weapon_manager.py`, make sure `WEAPON_TEXT_SOURCE` is the name of a text source in OBS

You can customize these sources freely to look good


At the start of `splatoon_weapons.py`, there is `weapon_manager.set_valid("variants")`

Use "base" just for original kis

Use "variants" for all kits, but not skins like Hero Shot

Use "all" for all weapons

Run `splatoon_weapons.py`

By Default

F1 = New Random Weapon (No Cooldown)

F2 = New Random Weapon (0.5 Second Cooldown)

F3 = Toggle whether sources are visible

F4 = New Random Weapon (Removes Picked Weapon from pool)

If you want to reset the pool, easiest way is to just restart the program
