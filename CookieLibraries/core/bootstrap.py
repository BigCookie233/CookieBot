# coding: utf-8
# Created by BigCookie233
import argparse
from functools import wraps

from typing import Callable

_initializers = []
_options = []
_args = None


def initializer(func: Callable) -> Callable:
    _initializers.append(func)
    return func


def optional(flag: str, help: str) -> Callable:
    _options.append((flag, help))

    def wrapper(func: Callable) -> Callable:
        @wraps(func)
        def wrap(*args, **kwargs):
            if _args.__getattr__(flag):
                func(*args, **kwargs)

        return func

    return wrapper


def get_arg(flag: str):
    return _args.__getattr__(flag)


def register(flag: str, help: str):
    _options.append((flag, help))

    def wrapper(func: Callable) -> Callable:
        return func

    return wrapper


def main():
    parser = argparse.ArgumentParser()
    for flag, help in _options:
        parser.add_argument(flag, help=help, action="store_true")
    _args = parser.parse_args()
    for func in _initializers:
        func()
