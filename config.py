import json
import os

config_path = os.path.join(os.path.dirname(__file__), "settings.json")

def _write_config(config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)
        f.write("\n")

def create_config():
    if not os.path.isfile(config_path):
        default_config = {
            "profil": {"default": []}
        }
        _write_config(default_config)

def read_config():
    if os.path.isfile(config_path):
        with open(config_path, "r") as f:
            try:
                return json.load(f)
            except json.JSONDecodeError:
                print("Warning: settings.json is malformed. Resetting to default.")
                create_config()
                return read_config()
    return {"profil": {"default": []}}

def write_config(price=None, profil=None, interval=None):
    config = read_config()

    if profil is not None:
        if not isinstance(profil, dict):
            raise ValueError("profil must be a dictionary")
        config.setdefault("profil", {}).update(profil)
    if interval is not None:
        config["interval"] = float(interval)

    _write_config(config)

def delete_profil(profil_name):
    config = read_config()
    profils = config.get("profil", {})

    if profil_name in profils:
        del profils[profil_name]
        config["profil"] = profils
        _write_config(config)
        print(f"Profil '{profil_name}' deleted successfully.")
    else:
        print(f"Profil '{profil_name}' not found.")