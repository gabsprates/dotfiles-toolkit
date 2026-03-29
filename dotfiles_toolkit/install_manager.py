import importlib
import sys
import os

from dotfiles_toolkit.app_installer import AppInstaller
from pathlib import Path
from typing import Dict, Type


class InstallManager:
    def __init__(self, *, apps_path: Path, distro: str):
        self.apps = []
        self.apps_path = apps_path.resolve()
        self.distro = distro

        self.__available_apps: Dict[str, Type[AppInstaller]] = {}

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

    def register(self, app_name: str):
        if (self.__available_apps.get(app_name) == None):
            raise KeyError()

        self.apps.append(app_name)

    def install_apps(self):
        """
        Runs app .install() and .customize() methods for all
        registered AppInstaller.
        """
        print(f"\n## Installing apps for: {self.distro.upper()}", '\n')

        for app_name in self.apps:
            app = self.__available_apps[app_name](
                os_id=self.distro
            )

            print(f">>> Install [{app_name}]: start")
            app.install()
            print(f">>> Install [{app_name}]: done", '\n')

            print(f">>> Customize [{app_name}]: start")
            app.customize()
            print(f">>> Customize [{app_name}]: done")
