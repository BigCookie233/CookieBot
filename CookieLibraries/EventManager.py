# coding: utf-8

# Created by BigCookie233

import inspect
from enum import Enum

event_listeners = {}


class Priority(Enum):
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4


class Event:
    def call(self):
        for module in event_listeners.values():
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        try:
                            listener(self)
                        except Exception as e:
                            print(e)


class CancellableEvent(Event):
    def __init__(self):
        self.isCancelled = False

    def cancel(self):
        self.isCancelled = True

    def call(self):
        for module in event_listeners.values():
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        if not self.isCancelled:
                            try:
                                listener(self)
                            except Exception as e:
                                print(e)


def event_listener(event_class, priority=Priority.NORMAL):
    if not isinstance(event_class, type) or not issubclass(event_class, Event):
        raise TypeError("event_listener() arg 1 must be a event class")
    if not isinstance(priority, Priority):
        raise TypeError("event_listener() arg 2 must be a priority")

    def wrapper(func):
        if len(inspect.signature(func).parameters) != 1:
            raise TypeError("The listener takes 0 positional arguments but 1 will be given")
        (event_listeners.setdefault(func.__module__, {})
         .setdefault(event_class, {})
         .setdefault(priority, []).append(func))
        return func

    return wrapper
