from json import dump, load
from os import mkdir, path, listdir, rename
from helpers import get_home_path, get_homebrew_path, get_user, get_user_group, get_user_owner, chown


class SettingsManager:
    def __init__(self, name, settings_directory = None) -> None:
        USER = get_user()
        GROUP = get_user_group()
        wrong_dir = get_homebrew_path()
        if settings_directory == None:
            settings_directory = path.join(wrong_dir, "settings")

        self.path = path.join(settings_directory, name + ".json")

        #Create the folder with the correct permission
        if not path.exists(settings_directory):
            mkdir(settings_directory)
            chown(settings_directory, USER, GROUP)

        #Copy all old settings file in the root directory to the correct folder
        for file in listdir(wrong_dir):
            if file.endswith(".json"):
                rename(path.join(wrong_dir,file),
                       path.join(settings_directory, file)) 
                self.path = path.join(settings_directory, name + ".json")


        #If the owner of the settings directory is not the user, then set it as the user:
        if get_user_owner(settings_directory) != USER:
            chown(settings_directory, USER, GROUP)

        self.settings = {}

        try:
            open(self.path, "x", encoding="utf-8")
        except FileExistsError as e:
            self.read()
            pass

    def read(self):
        try:
            with open(self.path, "r", encoding="utf-8") as file:
                self.settings = load(file)
        except Exception as e:
            print(e)
            pass

    def commit(self):
        with open(self.path, "w+", encoding="utf-8") as file:
            dump(self.settings, file, indent=4, ensure_ascii=False)

    def getSetting(self, key, default):
        return self.settings.get(key, default)

    def setSetting(self, key, value):
        self.settings[key] = value
        self.commit()
