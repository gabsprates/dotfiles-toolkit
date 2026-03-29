from dotfiles_toolkit.install_manager import InstallManager
from pathlib import Path


fake_apps_path = Path(__file__).parent.joinpath('fake_apps')


class TestInstallManager:

    def test_instantiation(self):

        install_manager = InstallManager(
            apps_path=fake_apps_path,
            distro='ubuntu',
        )

        assert install_manager.apps == []
        assert install_manager.apps_path == fake_apps_path.resolve()
        assert install_manager.distro == 'ubuntu'
        assert install_manager._InstallManager__available_apps.keys() == {
            'fake_app_a', 'fake_app_b',
        }

