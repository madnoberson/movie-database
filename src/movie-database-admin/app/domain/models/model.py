from typing import TypeVar


class Model:
    ...


ModelT = TypeVar("ModelT", bound=Model)