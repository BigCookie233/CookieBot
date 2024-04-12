# coding: utf-8

# Created by BigCookie233

import inspect
from typing import Callable


def exception_handler(handler) -> Callable:
    assert callable(handler), "the handler must be a callable object"
    params_len = len(inspect.signature(handler).parameters)
    assert params_len == 1, f"the handler takes {params_len} positional arguments but 1 and only 1 will be given"

    def wrapper(func) -> Callable:
        def catcher(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler(e)

        return catcher

    return wrapper


def forward_as(exception: Exception) -> Callable:
    def handler(exc: Exception):
        raise exception from exc

    return exception_handler(handler)
