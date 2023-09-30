import os
import toml
from typing import Type, TypeVar, Any

from pydantic import TypeAdapter


C = TypeVar("C")


def load_config(config_type: Type[C], path: str | os.PathLike | None = None) -> C:
    """
    Returns casted to `config_type` config loaded from `path` toml file
    if `path` is specified, otherwise loads config from local environment

    Raises
        * `ValidationError` if it is not possible to convert loaded config to `config_type`
        * `FileNotFoundError` if file doesn't exist
    """

    def load_toml(_path: str | os.PathLike) -> dict[str, Any]:
        with open(file=_path, mode="r", encoding="utf-8") as file:
            return toml.load(file)
        
    return TypeAdapter(config_type).validate_python(load_toml(path) if path else dict(os.environ))