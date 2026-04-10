import os
from pathlib import Path
from pathlike_typing import PathLike


class NuitkaBuilder:
    def __init__(self, config_path: PathLike):
        self.config_path = Path(config_path)
        

