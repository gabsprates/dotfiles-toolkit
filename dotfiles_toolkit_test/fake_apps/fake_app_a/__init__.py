from dotfiles_toolkit.app_installer import AppInstaller


class FakeAppAInstaller(AppInstaller):
    def __init__(self, os_id: str):
        pass

    def install(self):
        pass

    def customize(self):
        pass
