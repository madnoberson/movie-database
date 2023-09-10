from contextlib import contextmanager


@contextmanager
def f():
    yield 1


a = [f()]

for b in a:
    b.__enter__()


a[0].__enter__()