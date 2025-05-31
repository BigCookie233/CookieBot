# coding: utf-8
# Created by BigCookie233
import inspect
from functools import wraps

_providers = {}


class Provider:
    def __init__(self, func):
        assert callable(func), "invalid provider"
        sign = inspect.signature(func)
        self.__provider = func
        _providers[sign.return_annotation] = self

    def get(self):
        return inject(self.__provider)()

    @property
    def provider(self):
        return self.__provider


class SingletonProvider(Provider):
    def __init__(self, func):
        super().__init__(func)
        self.__instance = None

    def get(self):
        if self.__instance is None:
            self.__instance = super().get()
        return self.__instance


def provider(func) -> Provider:
    return Provider(func)


def singleton(func) -> SingletonProvider:
    return SingletonProvider(func)


def inject(func):
    dependencies = {}
    sign = inspect.signature(func)
    mode = 0
    for name, param in sign.parameters.items():
        if param.default == inject and mode == 0:
            dependencies.clear()
            mode = 1
        if mode == 0 or param.default == inject:
            dependencies[name] = param.annotation

    @wraps(func)
    def wrapper(*args, **kwargs):
        return func(*args, **kwargs, **{key: _providers[value].get() for key, value in dependencies.items()})

    return wrapper
