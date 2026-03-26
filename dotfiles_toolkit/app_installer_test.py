import json
import pytest
import tempfile
import urllib.request

from .app_installer import AppInstaller
from pathlib import Path


class FakeResponse:
    def __init__(self, payload: dict):
        self.payload = payload

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc, tb):
        pass

    def read(self):
        return json.dumps(self.payload).encode("utf-8")


@pytest.fixture
def fake_github_response():
    return lambda payload: FakeResponse(payload)


@pytest.fixture
def fake_mkdtemp(monkeypatch, tmp_path):
    def _mock():
        path = tmp_path.joinpath('temp_dir')
        path.mkdir(exist_ok=True)
        return path

    monkeypatch.setattr(tempfile, "mkdtemp", _mock)

    return _mock


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

    def test_create_temp_path(self, fake_mkdtemp):
        temp_dir = AppInstaller.create_temp_path()

        assert temp_dir.exists()
        assert temp_dir.is_dir()

    def test_create_temp_path_with_path(self, fake_mkdtemp):
        temp_file = AppInstaller.create_temp_path('my_file.txt')
        temp_file.touch()

        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.name == 'my_file.txt'

    def test_get_asset_url_from_github_success(self, monkeypatch, fake_github_response):
        payload = {
            "assets": [
                {
                    "browser_download_url": "https://github.com/owner/repo/asset/dotfiles_toolkit_LINUX_x86_64.tar.gz"
                },
            ]
        }

        monkeypatch.setattr(
            urllib.request,
            "urlopen",
            lambda _: fake_github_response(payload)
        )

        release_url = AppInstaller.get_asset_url_from_github(
            owner="gabsprates",
            repo="dotfiles_toolkit",
            filter=lambda url: url.lower().endswith("_linux_x86_64.tar.gz"),
        )

        assert release_url == payload["assets"][0]["browser_download_url"]

    def test_get_asset_url_from_github_not_found(self, monkeypatch, fake_github_response):
        payload = {
            "assets": [
                {
                    "browser_download_url": "https://github.com/owner/repo/asset/dotfiles_toolkit_LINUX_x86_64.zip"
                },
            ]
        }

        monkeypatch.setattr(
            urllib.request,
            "urlopen",
            lambda _: fake_github_response(payload)
        )

        with pytest.raises(FileNotFoundError):
            _ = AppInstaller.get_asset_url_from_github(
                owner="gabsprates",
                repo="dotfiles_toolkit",
                filter=lambda url: url.lower().endswith("_linux_x86_64.tar.gz"),
            )

    def test_download(self, monkeypatch, tmp_path):
        def fake_mkdtemp():
            return tmp_path

        def fake_urlretrieve(url, filename):
            temp_file = tmp_path.joinpath(filename)
            temp_file.touch()
            return temp_file, None

        monkeypatch.setattr(tempfile, "mkdtemp", fake_mkdtemp)
        monkeypatch.setattr(urllib.request, "urlretrieve", fake_urlretrieve)

        filename = "asset.tar.gz"

        temp_file = AppInstaller.download(
            "https://example.com/download/asset.tar.gz",
            filename
        )

        assert temp_file.exists()
        assert temp_file.is_file()
        assert temp_file.name == filename
