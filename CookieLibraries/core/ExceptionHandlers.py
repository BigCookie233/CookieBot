# coding: utf-8

# Created by BigCookie233

import inspect
from typing import Callable


def exception_handler(handler: Callable) -> Callable:
    assert callable(handler), "the handler must be a callable object"
    params_len = len(inspect.signature(handler).parameters)
    assert params_len > 1, f"the handler takes {params_len} positional arguments but only 1 at most will be given"

    def wrapper(func: Callable) -> Callable:
        def catcher(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as exc:
                if params_len == 1:
                    handler(exc)
                else:
                    handler()

        return catcher

    return wrapper


def forward_as(exception: Exception) -> Callable:
    def handler(exc: Exception):
        raise exception from exc

    return exception_handler(handler)
