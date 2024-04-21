import os
import toml
from typing import Any


class Config:
    def __init__(self, filepath: str) -> None:
        assert os.path.isfile(filepath), f"Config file '{filepath}' does not exist."
        self._config = toml.load(filepath)

    def __getattr__(self, name: str) -> Any:
        return self._config[name]