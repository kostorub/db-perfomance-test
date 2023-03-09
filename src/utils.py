import functools
from time import time


def timeitit(func):
    @functools.wraps(func)
    def wrapper_timeit(*args, **kwargs):
        ts = time()
        result = func(*args, **kwargs)
        print(f"Timeitit <{func.__name__}>: {time() - ts} sec")
        return result

    return wrapper_timeit
