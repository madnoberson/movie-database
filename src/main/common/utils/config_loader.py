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

    def from_toml(_config_type: Type[C], _path: str | os.PathLike) -> C:
        with open(file=_path, mode="r", encoding="utf-8") as file:
            return TypeAdapter(_config_type).validate_python(toml.load(file))
    
    def from_enviroment(_config_type: Type[C]) -> C:
        config_fields = {}
        for name, field_type in config_type.__annotations__.items():
            value = TypeAdapter(field_type).validate_python(dict(os.environ))
            config_fields.update({name: value})
        return _config_type(**config_fields)

    return from_toml(config_type, path) if path else from_enviroment(config_type)
