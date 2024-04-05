# coding: utf-8

# Created by BigCookie233

import inspect


def exception_dispatcher(handler, block: bool = False):
    if not callable(handler):
        raise TypeError("the handler must be a callable object")
    params_len = len(inspect.signature(handler).parameters)
    if params_len != 1:
        raise TypeError("the handler takes {} positional arguments but 1 and only 1 will be given".format(params_len))

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
