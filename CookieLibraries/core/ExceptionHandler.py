# coding: utf-8

# Created by BigCookie233

import inspect


def exception_dispatcher(handler, block: bool = False):
    assert callable(handler), "the handler must be a callable object"
    params_len = len(inspect.signature(handler).parameters)
    assert params_len == 1, f"the handler takes {params_len} positional arguments but 1 and only 1 will be given"

    def wrapper(func):
        def dispatcher(*args, **kwargs):
            try:
                return func(*args, **kwargs)
            except Exception as e:
                handler(e)
                if not block:
                    raise

        return dispatcher

    return wrapper