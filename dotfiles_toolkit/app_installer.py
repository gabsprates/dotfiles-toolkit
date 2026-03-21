import json
import os
import tempfile
import urllib.request

from collections.abc import Callable
from pathlib import Path


class AppInstaller:
    """
    Interface to be implemented for each app that should be installed.
    """

    def __init__(self, os_id: str):
        raise NotImplementedError(
            "Plugins must implement the '__init__' method.")

    def install(self):
        """
        Method that executes any sudo actions, as instaling packages.
        """
        raise NotImplementedError(
            "Plugins must implement the 'install' method.")

    def customize(self):
        """
        Method that execcutes any user level customization, like editing
        PATH, or even installing something at user's directory.
        """
        raise NotImplementedError(
            "Plugins must implement the 'customize' method.")

    @staticmethod
    def create_symlink(link: Path, target: Path) -> None:
        if link.is_file():
            os.remove(link)

        link.symlink_to(target)

    @staticmethod
    def create_temp_path(path: str | None = None) -> Path:
        root_dir = Path(tempfile.mkdtemp())

        if path:
            return root_dir.joinpath(path)

        return root_dir

    @staticmethod
    def get_asset_url_from_github(
        owner: str,
        repo: str,
        filter: Callable[[str], bool],
    ) -> str:
        url_releases = f"https://api.github.com/repos/{owner}/{repo}/releases/latest"

        with urllib.request.urlopen(url_releases) as response:
            json_data = json.loads(response.read().decode())

            for asset in json_data['assets']:
                if filter(asset['browser_download_url']):
                    return asset['browser_download_url']

        raise FileNotFoundError()

    @staticmethod
    def download(url: str, filename: str) -> Path:
        temp_file = AppInstaller.create_temp_path(filename)

        actual_file, _ = urllib.request.urlretrieve(url, temp_file)

        return Path(actual_file)
