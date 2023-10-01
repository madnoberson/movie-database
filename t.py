class A:
    ...


class B(A):

    ...

from typing import AsyncContextManager, get_origin, get_args
class C:

    def f(self) -> AsyncContextManager[B]:
        ...


print()
print(issubclass(get_args(C.f.__annotations__["return"])[0], A))