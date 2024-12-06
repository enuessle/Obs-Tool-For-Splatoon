import time
import sys
from obswebsocket import obsws,requests

#Largely Created From https://github.com/DougDougGithub/Babagaboosh

WEBSOCKET_HOST = "localhost"

#Manager To Interact With OBS Through an OBSWebsocket
class OBSManager:
    ws = None

    def __init__(self, port, password):
        #Initilization
        self.ws = obsws(WEBSOCKET_HOST, port, password)
        try:
            self.ws.connect()
        except Exception as e:
            print("COULD NOT CONNECT TO OBS!\nDouble check that you have OBS open and that your websockets server is enabled in OBS.")
            raise Exception("Could Not Connect To OBS")
        print("Connected to OBS Websockets!\n")

    def disconnect(self):
        self.ws.disconnect()

    # Set the current scene
    def set_scene(self, new_scene):
        self.ws.call(requests.SetCurrentProgramScene(sceneName=new_scene))

    # Set the visibility of any source's filters
    def set_filter_visibility(self, source_name, filter_name, filter_enabled=True):
        self.ws.call(requests.SetSourceFilterEnabled(sourceName=source_name, filterName=filter_name, filterEnabled=filter_enabled))

    # Change a sources visibility
    # Default to True
    def set_source_visibility(self, scene_name, source_name, source_visibility=True):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        myItemID = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemEnabled(sceneName=scene_name,sceneItemId=myItemID, sceneItemEnabled=source_visibility))

    # Returns the current text of a text source
    def get_text(self, source_name):
        response = self.ws.call(requests.GetInputSettings(inputName=source_name))
        return response.datain["inputSettings"]["text"]

    # Sets the text of a text source
    def set_text(self, source_name, new_text):
        self.ws.call(requests.SetInputSettings(inputName=source_name, inputSettings = {'text': new_text}))


    # Returns the current file path of an image source
    def get_file(self, source_name):
        response = self.ws.call(requests.GetInputSettings(inputName=source_name))
        return response.datain["inputSettings"]["file"]
    
    # Sets the file of an image source
    def set_file(self, source_name, file_path):
        self.ws.call(requests.SetInputSettings(inputName=source_name, inputSettings = {'file': file_path}))

    # Return Transformation Properties of a Source
    def get_source_transform(self, scene_name, source_name):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        myItemID = response.datain['sceneItemId']
        response = self.ws.call(requests.GetSceneItemTransform(sceneName=scene_name, sceneItemId=myItemID))
        transform = {}
        transform["positionX"] = response.datain["sceneItemTransform"]["positionX"]
        transform["positionY"] = response.datain["sceneItemTransform"]["positionY"]
        transform["scaleX"] = response.datain["sceneItemTransform"]["scaleX"]
        transform["scaleY"] = response.datain["sceneItemTransform"]["scaleY"]
        transform["rotation"] = response.datain["sceneItemTransform"]["rotation"]
        transform["sourceWidth"] = response.datain["sceneItemTransform"]["sourceWidth"] # original width of the source
        transform["sourceHeight"] = response.datain["sceneItemTransform"]["sourceHeight"] # original width of the source
        transform["width"] = response.datain["sceneItemTransform"]["width"] # current width of the source after scaling, not including cropping. If the source has been flipped horizontally, this number will be negative.
        transform["height"] = response.datain["sceneItemTransform"]["height"] # current height of the source after scaling, not including cropping. If the source has been flipped vertically, this number will be negative.
        transform["cropLeft"] = response.datain["sceneItemTransform"]["cropLeft"] # the amount cropped off the *original source width*. This is NOT scaled, must multiply by scaleX to get current # of cropped pixels
        transform["cropRight"] = response.datain["sceneItemTransform"]["cropRight"] # the amount cropped off the *original source width*. This is NOT scaled, must multiply by scaleX to get current # of cropped pixels
        transform["cropTop"] = response.datain["sceneItemTransform"]["cropTop"] # the amount cropped off the *original source height*. This is NOT scaled, must multiply by scaleY to get current # of cropped pixels
        transform["cropBottom"] = response.datain["sceneItemTransform"]["cropBottom"] # the amount cropped off the *original source height*. This is NOT scaled, must multiply by scaleY to get current # of cropped pixels
        return transform
    
    # The transform should be a dictionary containing any of the following keys with corresponding values
    # positionX, positionY, scaleX, scaleY, rotation, width, height, sourceWidth, sourceHeight, cropTop, cropBottom, cropLeft, cropRight
    # e.g. {"scaleX": 2, "scaleY": 2.5}
    # Note: there are other transform settings, like alignment, etc, but these feel like the main useful ones.
    # Use get_source_transform to see the full list
    def set_source_transform(self, scene_name, source_name, new_transform):
        response = self.ws.call(requests.GetSceneItemId(sceneName=scene_name, sourceName=source_name))
        myItemID = response.datain['sceneItemId']
        self.ws.call(requests.SetSceneItemTransform(sceneName=scene_name, sceneItemId=myItemID, sceneItemTransform=new_transform))


    # Note: an input, like a text box, is a type of source. This will get *input-specific settings*, not the broader source settings like transform and scale
    # For a text source, this will return settings like its font, color, etc
    def get_input_settings(self, input_name):
        return self.ws.call(requests.GetInputSettings(inputName=input_name))

    # Get list of all items in a certain scene
    def get_scene_items(self, scene_name):
        return self.ws.call(requests.GetSceneItemList(sceneName=scene_name))


#Testing Code
if __name__ == '__main__':
    print("Testing OBS Websockets")

    obs_manager = OBSManager("4455", "Splatoon")

    print("Testing Scene Change")
    obs_manager.set_scene("Test")
    time.sleep(2)

    print("Changing Caption")
    obs_manager.set_text("* Caption", "First Test")
    time.sleep(2)
    obs_manager.set_text("* Caption", "Second Test")
    time.sleep(2)
    obs_manager.set_text("* Caption", "Third Test")
    time.sleep(2)

    print("Transform Tests")
    transforms = obs_manager.get_source_transform("Test", "* Caption")
    print(transforms)
    time.sleep(1)

    print("Input Settings Test")
    input_settings = obs_manager.get_input_settings("Test Image")
    print(input_settings)
    time.sleep(1)

    print("Test File Changes")
    filepath = obs_manager.get_file("Test Image")
    print(filepath)
    time.sleep(1)
    obs_manager.set_file("Test Image", "C:/Users/Ethan/Pictures/Content Assets/Extra Assets/Splatoon-3-Side-Order-1.jpg")
    time.sleep(2)
    obs_manager.set_file("Test Image", "C:/Users/Ethan/Pictures/Content Assets/Extra Assets/Splatoon-3-Review-Chaotic-Refreshing-Fun-Switch-Turfwar.jpg")
    time.sleep(2)
    

    obs_manager.disconnect()

