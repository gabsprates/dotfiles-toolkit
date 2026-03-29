from dotfiles_toolkit.app_installer import AppInstaller


class FakeAppAInstaller(AppInstaller):
    def __init__(self, os_id: str):
        pass

    def install(self):
        AppInstaller.create_temp_path('fake_app_a.install').touch()
        pass

    def customize(self):
        AppInstaller.create_temp_path('fake_app_a.customize').touch()
        pass
