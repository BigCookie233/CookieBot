# coding: utf-8

# Created by BigCookie233

from typing import Callable
import pickle


class Cacher:
    def __init__(self, func: Callable, maxsize: int):
        assert callable(func), "the function must be a callable object"
        self.func = func
        self.maxsize = maxsize
        self.hits = 0
        self.misses = 0
        self.mappings = {}

    def __call__(self, *args, **kwargs):
        params = pickle.dumps((args, kwargs))
        if params in self.mappings:
            self.hits += 1
            return self.mappings[params]
        self.misses += 1
        result = self.func(*args, **kwargs)
        self.cache(args, kwargs, result)
        return result

    def cache(self, args, kwargs, result):
        params = pickle.dumps((args, kwargs))
        if len(self.mappings) >= self.maxsize:
            for key in list(self.mappings.keys())[:len(self.mappings) - self.maxsize]:
                self.mappings.pop(key)
        self.mappings[params] = result

    def reset(self):
        self.mappings = {}
        self.hits = 0
        self.misses = 0


def cache(maxsize: int = 20) -> Callable:
    def cacher(func) -> Cacher:
        return Cacher(func, maxsize)

    return cacher
