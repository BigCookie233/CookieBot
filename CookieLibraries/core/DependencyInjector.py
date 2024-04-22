# coding: utf-8

# Created by BigCookie233

_beans = {}


class Bean:
    def __init__(self, func):
        assert (callable(func)
                and hasattr(func, "__annotations__")
                and "return" in func.__annotations__), "invalid factory"
        self.__func = func
        self.__instance = None
        _beans[func.__annotations__.get("return")] = self

    def __call__(self):
        self.__func()

    @property
    def instance(self):
        if self.__instance is None:
            self.__instance = inject(self.__func)()
        return self.__instance


def bean(func):
    return Bean(func)


def inject(func):
    def wrapper():
        kwargs = {}
        for name, clazz in func.__annotations__.items():
            if name != "return":
                kwargs[name] = _beans[clazz].instance
        return func(**kwargs)

    return wrapper
