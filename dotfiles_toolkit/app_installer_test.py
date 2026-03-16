import random

from pathlib import Path
from .app_installer import AppInstaller


class TestAppInstaller:

    def test_create_symlink(self, tmp_path: Path):
        file_target = tmp_path.joinpath('file_target')
        file_link = tmp_path.joinpath('file_link')

        file_target.write_text(str(random.random()))

        assert not file_link.exists()

        AppInstaller.create_symlink(
            link=file_link,
            target=file_target
        )

        assert file_link.exists()

        assert file_link.is_symlink()

        assert file_link.resolve() == file_target.resolve()
