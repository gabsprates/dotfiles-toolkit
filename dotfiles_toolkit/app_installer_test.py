from pathlib import Path
from .app_installer import AppInstaller


class TestAppInstaller:

    def test_create_symlink(self, tmp_path: Path):
        file_target = tmp_path.joinpath('file_target')
        file_link = tmp_path.joinpath('file_link')

        file_target.write_text("test")

        assert not file_link.exists()

        AppInstaller.create_symlink(
            link=file_link,
            target=file_target
        )

        assert file_link.exists()

        assert file_link.is_symlink()

        assert file_link.resolve() == file_target.resolve()

    def test_create_temp_path(self):
        temp_dir, temp_file = AppInstaller.create_temp_path()

        assert temp_dir.exists()
        assert temp_dir.is_dir()
        assert temp_file == None

        temp_dir.rmdir()

    def test_create_temp_path_with_path(self):
        temp_dir, temp_file = AppInstaller.create_temp_path('my_file.txt')
        temp_file.touch()

        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.name == 'my_file.txt'

        temp_file.unlink()
        temp_dir.rmdir()
