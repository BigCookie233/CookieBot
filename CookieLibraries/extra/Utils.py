# coding: utf-8
# Created by BigCookie233
from typing import Callable


def allow_default(func) -> Callable:
    def wrapper(*args, **kwargs):
        if len(args) == 1 and callable(args[0]):
            return func(args[0])
        else:
            return lambda func_: func(func_, *args, **kwargs)

    return wrapper
