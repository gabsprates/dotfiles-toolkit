import importlib
import sys
import os

from dotfiles_toolkit.app_installer import AppInstaller
from pathlib import Path


class InstallManager:
    def __init__(self, *, apps_path: Path, distro: str):
        self.apps = []
        self.apps_path = apps_path.resolve()
        self.distro = distro

        self.__available_apps = {}

        sys.path.append(str(self.apps_path))

        for app_name in os.listdir(self.apps_path):
            module = importlib.import_module(app_name)

            for attribute in dir(module):
                app_class = (getattr(module, attribute))

                if (isinstance(app_class, type)
                        and issubclass(app_class, AppInstaller)
                        and app_class is not AppInstaller):

                    self.__available_apps.update({
                        app_name: app_class
                    })

