from configparser import ConfigParser
import os

config = ConfigParser()

def createConfig():
    config_path = os.path.join(os.path.dirname(__file__), "settings.ini")
    if not os.path.isfile(config_path):
        config["DEFAULT"] = {
            "size": "670,385",
            "pos": "300,300"
        }
        config["PROFIL"] = {
            "selected_classes": ['Shadow Hunter', 'Boomeranger', 'Dracolyte']
        }
        with open(config_path, "w") as f:
            config.write(f)

def writeConfig(size=None, pos=None, selected_classes=None):
    config_path = os.path.join(os.path.dirname(__file__), "settings.ini")
    config.read(config_path)

    if size:
        config.set("DEFAULT", "size", size)
    if pos:
        config.set("DEFAULT", "pos", pos)
    if selected_classes:
        selected_classes = [class_name.strip() for class_name in selected_classes]
        config.set("PROFIL", "selected_classes",str(selected_classes))

    with open(config_path, "w") as f:
        config.write(f)

def readConfig():
    config_path = os.path.join(os.path.dirname(__file__), "settings.ini")
    config.read(config_path)

    size = config["DEFAULT"].get("size", "670,385")
    pos = config["DEFAULT"].get("pos", "300,300")
    selected_classes = config["PROFIL"].get("selected_classes", "")  # Ajout de cette ligne

    return {
        "size": [int(i) for i in size.split(",")],
        "pos": [int(i) for i in pos.split(",")],
        "selected_classes": selected_classes.split(",")  # Modification de cette ligne
    }
