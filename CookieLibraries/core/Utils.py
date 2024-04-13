# coding: utf-8

# Created by BigCookie233

from typing import Callable


def allow_default(func) -> Callable:
    def wrapper(*args, **kwargs):
        if not args:
            return lambda func_: func(func_, **kwargs)
        elif len(args) == 1 and callable(args[0]):
            return func(args[0])
        else:
            raise ValueError("invalid parameters")

    return wrapper
