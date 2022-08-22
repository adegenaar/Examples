"""
    Settings object
"""

import json
import os


class Settings:
    """
    Settings Manager
    """

    _config_location = "config.json"

    def __init__(self):
        if os.path.exists(self._config_location):
            with open(self._config_location, encoding="utf-8") as settings_file:
                self.__dict__ = json.load(settings_file)
        else:
            self.__dict__ = {"settingA": "myDefaultSettingA", "settingB": "myDefaultSettingB"}

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        with open(self._config_location, "w", encoding="utf-8") as settings_file:
            json.dump(self.__dict__, settings_file, indent=4)


if __name__ == "__main__":
    with Settings() as settings:
        # Those settings will be saved (with eventual modifications)
        # when script exits
        settings.settingA = "myNewSettingA"
