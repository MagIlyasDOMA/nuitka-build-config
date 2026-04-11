import os
from pathlib import Path
from pathlike_typing import PathLike
from .descriptors import CachedProperty, UncacheProperty
from .models import NuitkaConfig


class NuitkaBuilder:
    config_path: Path = UncacheProperty('config', 'command')

    def __init__(self, config_path: PathLike = 'nbc-config.yaml'):
        self.config_path = Path(config_path)

    @CachedProperty
    def config(self) -> NuitkaConfig:
        return NuitkaConfig.from_yaml_file(self.config_path)

    @CachedProperty
    def command(self) -> str:
        config = self.config

