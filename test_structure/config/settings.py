# Handles loading/saving user settings (JSON)
import os 
from pathlib import Path
import json
class ManageSettings:
    def __init__(self) -> None:
        self.place_to_store = os.getenv("APPDATA") or os.path.expanduser("~")
        self.config_dir = Path(self.place_to_store)/"BatteryLimiter5"
        self.config_dir.mkdir(exist_ok=True)
        self.config_file = self.config_dir/"settings.json"
    def save_settings(self):
        test_dict = {"min":20,"max":80}
        try:
            with open(self.config_file, "w") as set:
                json.dump(test_dict,set,indent=2)
            return True
        except Exception as e:
            return f"Something went wrong {e}, {e.__str__}"
    def get_settings(self):
        try:
            with open(self.config_file,"r") as set:
                all_settings = json.load(set)
                return all_settings
        except Exception as e:
            return f"Something went wrong {e}, {e.__str__}"
