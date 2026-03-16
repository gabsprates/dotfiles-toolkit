# Dotfiles Toolkit

[![GitHub tag](https://img.shields.io/github/tag/gabsprates/dotfiles-toolkit.svg)](https://GitHub.com/gabsprates/dotfiles-toolkit/tags/)

Add to your dotfiles' `requirements.txt`:

```
dotfiles_toolkit @ git+https://github.com/gabsprates/dotfiles-toolkit@0.1.0
```

And use it in your plugin:

```python
# plugins/terminator
# ├── __init__.py
# └── profile

import subprocess

from pathlib import Path
from dotfiles_toolkit.app_installer import AppInstaller


class TerminatorInstaller(AppInstaller):
    def __init__(self, os_id: str):
        self.plugin_path = Path(__file__).parent.resolve()

    def install(self):
        subprocess.run(['sudo', 'add-apt-repository',
                       'ppa:mattrose/terminator'])
        subprocess.run(['sudo', 'apt-get', 'update'])
        subprocess.run(['sudo', 'apt', 'install', '-y', 'terminator'])

    def customize(self):
        AppInstaller.create_symlink(
            link=Path('/home/me/.config/terminator/config'),
            target=self.plugin_path.joinpath('profile')
        )
```

## WIP

- [ ] AppInstaller
  - [ ] downlaod
  - [ ] temp path
- [ ] Plugin loader
