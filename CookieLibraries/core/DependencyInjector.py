# coding: utf-8
# Created by BigCookie233
import inspect
from functools import wraps

from .Bootstrap import bootstrap

_providers = {}


class Provider:
    def __init__(self, func):
        assert callable(func), "invalid provider"
        sign = inspect.signature(func)
        self.__func = func
        self.__instance = None
        _providers[sign.return_annotation] = self

    def get_instance(self):
        if self.__instance is None:
            self.__instance = inject(self.__func)()
        return self.__instance


def get_instance_A(clazz):
    return _providers[clazz].get_instance()


def provider(func) -> Provider:
    return Provider(func)


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
        return func(*args, **kwargs, **{key: _providers[value].get_instance() for key, value in dependencies.items()})

    return wrapper


@bootstrap
def initialize_all_providers():
    for clazz in _providers:
        _providers[clazz].get_instance()
