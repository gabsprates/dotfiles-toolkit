import os
import tempfile

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
    def create_temp_path(path: str | None = None) -> tuple[Path, Path | None]:
        root_dir = Path(tempfile.mkdtemp())

        if path:
            return root_dir, root_dir.joinpath(path)

        return root_dir, None
