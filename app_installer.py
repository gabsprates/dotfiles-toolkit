import os

from pathlib import Path


class AppInstaller:

    @staticmethod
    def create_symlink(link: Path, target: Path):
        if link.is_file():
            os.remove(link)

        link.symlink_to(target)
