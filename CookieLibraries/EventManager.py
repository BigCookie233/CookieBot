# coding: utf-8

# Created by BigCookie233

import inspect
from enum import Enum

import CookieLibraries.LoggerManager as LoggerManager

event_listeners = {}


class Priority(Enum):
    """
    Available priorities
    """
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4


class Event:
    """
    Event base class
    """
    def call(self):
        """
        Call event
        """
        for module in event_listeners.values():
            for clazz in module:
                if issubclass(self.__class__, clazz):
                    for priority in sorted(module[clazz].keys(), key=lambda x: x.value):
                        for listener in module[clazz][priority]:
                            LoggerManager.traceback_exception(True)(listener)(self)


class CancellableEvent(Event):
    """
    Cancellable event base class
    """
    def __init__(self):
        self.isCancelled = False

    def cancel(self):
        """
        Cancel event
        """
        self.isCancelled = True

    def call(self):
        """
        Call event
        """
        for module in event_listeners.values():
            for clazz in module:
                if issubclass(self.__class__, clazz):
                    for priority in sorted(module[clazz].keys(), key=lambda x: x.value):
                        for listener in module[clazz][priority]:
                            LoggerManager.traceback_exception(True)(listener)(self)
                            if self.isCancelled:
                                return None


def event_listener(event_class: type, priority: Priority = Priority.NORMAL):
    """
    Register event listener

    Args:
        event_class (type): The event
        priority (Priority): The priority of this listener
    """
    if not isinstance(event_class, type) or not issubclass(event_class, Event):
        raise TypeError("event_listener() arg 1 must be a event class")
    if not isinstance(priority, Priority):
        raise TypeError("event_listener() arg 2 must be a priority")

    def wrapper(func):
        params_len = len(inspect.signature(func).parameters)
        if params_len != 1:
            raise TypeError(
                "the listener takes {} positional arguments but 1 and only 1 will be given".format(params_len))
        (event_listeners.setdefault(func.__module__, {})
         .setdefault(event_class, dict())
         .setdefault(priority, []).append(func))
        return func

    return wrapper


def unregister_listener(func):
    """
    Unregister event listener

    Args:
        func: The listener
    """
    for module in event_listeners.values():
        for clazz in module.values():
            for listeners in clazz.values():
                if func in listeners:
                    listeners.remove(func)


def unregister_module(module):
    """
    Unregister all listeners of a module

    Args:
        module: The module
    """
    event_listeners.pop(module)
