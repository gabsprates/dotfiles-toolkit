import os
from pathlib import Path

from .app_installer import AppInstaller


def test_app_installer_create_symlink():

    file_target = Path('/tmp/file_target')
    file_link = Path('/tmp/file_link')

    os.remove(file_link)
    os.remove(file_target)

    with open(file_target, 'w') as file:
        file.write("target file")

    assert file_link.exists() == False

    AppInstaller.create_symlink(
        link=file_link,
        target=file_target
    )

    assert file_link.exists() == True

    assert file_link.is_symlink() == True

    assert file_link.resolve() == file_target.resolve()

    os.remove(file_link)
    os.remove(file_target)
