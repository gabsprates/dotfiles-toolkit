import json
import pytest
import tempfile
import urllib.request

from .app_installer import AppInstaller
from pathlib import Path


def makeFakeResponse(mockreturn):
    class FakeResponse:
        def __enter__(self):
            return self

        def __exit__(self, exc_type, exc, tb):
            pass

        def read(self):
            return json.dumps(mockreturn).encode("utf-8")

    return FakeResponse()


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

    def test_create_temp_path(self, monkeypatch):
        def fake_mkdtemp():
            temp_path = Path("/tmp/temp_test")
            temp_path.mkdir()
            return temp_path

        monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)

        temp_dir = AppInstaller.create_temp_path()

        assert temp_dir.exists()
        assert temp_dir.is_dir()

        temp_dir.rmdir()

    def test_create_temp_path_with_path(self, monkeypatch):
        def fake_mkdtemp():
            temp_path = Path("/tmp/temp_test")
            temp_path.mkdir()
            return temp_path

        monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)

        temp_file = AppInstaller.create_temp_path('my_file.txt')
        temp_file.touch()

        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.name == 'my_file.txt'

        temp_file.unlink()
        temp_file.parent.rmdir()

    def test_get_asset_url_from_github(self, monkeypatch):
        mockreturn = {
            "assets": [
                {
                    "browser_download_url": "https://github.com/owner/repo/asset/dotfiles_toolkit_LINUX_x86_64.tar.gz"
                },
            ]
        }

        def fake_urlopen(url):
            return makeFakeResponse(mockreturn)

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

        release_url = AppInstaller.get_asset_url_from_github(
            owner="gabsprates",
            repo="dotfiles_toolkit",
            filter=lambda url: url.lower().endswith("_linux_x86_64.tar.gz"),
        )

        assert release_url == mockreturn["assets"][0]["browser_download_url"]

    def test_get_asset_url_from_github_error(self, monkeypatch):
        mockreturn = {
            "assets": [
                {
                    "browser_download_url": "https://github.com/owner/repo/asset/dotfiles_toolkit_LINUX_x86_64.zip"
                },
            ]
        }

        def fake_urlopen(url):
            return makeFakeResponse(mockreturn)

        monkeypatch.setattr(urllib.request, "urlopen", fake_urlopen)

        with pytest.raises(FileNotFoundError):
            _ = AppInstaller.get_asset_url_from_github(
                owner="gabsprates",
                repo="dotfiles_toolkit",
                filter=lambda url: url.lower().endswith("_linux_x86_64.tar.gz"),
            )

    def test_download(self, monkeypatch):
        base_temp_dir = Path("/tmp/temp_test")

        def fake_mkdtemp():
            temp_path = base_temp_dir
            temp_path.mkdir()
            return temp_path

        def fake_urlretrieve(url, filename):
            temp_file = base_temp_dir.joinpath(filename)
            temp_file.touch()
            return temp_file

        monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)
        monkeypatch.setattr(urllib.request, "urlretrieve", fake_urlretrieve)

        url = "https://github.com/asdf-vm/asdf/releases/download/v0.18.1/asdf-v0.18.1-darwin-arm64.tar.gz"
        filename = "asdf.tar.gz"

        temp_file = AppInstaller.download(url, filename)

        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.name == filename

        temp_file.unlink()
        temp_file.parent.rmdir()
