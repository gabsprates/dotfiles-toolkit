import tempfile

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

    def test_register_app(self):
        install_manager = InstallManager(
            apps_path=fake_apps_path,
            distro='ubuntu',
        )

        install_manager.register('fake_app_a')

        assert install_manager.apps == ['fake_app_a']

    def test_install_app(self, monkeypatch, tmp_path: Path):
        def fake_mkdtemp():
            return tmp_path

        monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)

        install_manager = InstallManager(
            apps_path=fake_apps_path,
            distro='ubuntu',
        )

        install_manager.register('fake_app_a')

        assert not tmp_path.joinpath('fake_app_a.install').exists()
        assert not tmp_path.joinpath('fake_app_a.customize').exists()

        install_manager.install_apps()

        assert tmp_path.joinpath('fake_app_a.install').exists()
        assert tmp_path.joinpath('fake_app_a.customize').exists()
