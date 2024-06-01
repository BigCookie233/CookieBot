# coding: utf-8

# Created by BigCookie233

import inspect
from functools import wraps

_beans = {}


class Bean:
    def __init__(self, func):
        assert callable(func), "invalid bean"
        sign = inspect.signature(func)
        self.__func = func
        self.__instance = None
        _beans[sign.return_annotation] = self

    @property
    def instance(self):
        if self.__instance is None:
            self.__instance = autowired(self.__func)()
        return self.__instance


def get_instance(clazz) -> Bean:
    return _beans[clazz].instance


def bean(func) -> Bean:
    return Bean(func)


def autowired(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        dependencies = {}
        sign = inspect.signature(func)
        mode = 0
        for name, param in sign.parameters.items():
            if param.default == autowired and mode == 0:
                dependencies.clear()
                mode = 1
            if mode == 0 or param.default == autowired:
                dependencies[name] = param.annotation
        return func(*args, **kwargs, **{key: _beans[value].instance for key, value in dependencies.items()})

    return wrapper


def initialize_all_beans():
    for i in _beans:
        get_instance(i)
