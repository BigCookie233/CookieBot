# coding: utf-8

# Created by BigCookie233

import inspect
import warnings
from enum import Enum
from typing import Callable

import CookieLibraries.core.LoggerManager as LoggerManager

event_listeners = {}


class Priority(Enum):
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
            for clazz, listeners in module.items():
                if issubclass(self.__class__, clazz):
                    for listener in listeners:
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
            for clazz, listeners in module.items():
                if issubclass(self.__class__, clazz):
                    for listener in listeners:
                        LoggerManager.traceback_exception(True)(listener)(self)
                        if self.isCancelled:
                            return None


class EventListener:
    def __init__(self, listener: Callable, event_class: type, priority: Priority):
        assert callable(listener), "the listener must be a callable object"
        params_len = len(inspect.signature(listener).parameters)
        assert params_len == 1, f"the listener takes {params_len} positional arguments but 1 and only 1 will be given"
        assert isinstance(event_class, type) and issubclass(event_class, Event), "the event_class must be a event class"
        assert isinstance(priority, Priority), "the priority must be a priority"
        self.listener = listener
        self.event_class = event_class
        self.priority = priority

    def __call__(self, event: Event):
        self.listener(event)

    def unregister(self):
        """
        Unregister the event listener
        """
        for module in event_listeners.values():
            for clazz, listeners in module.items():
                if self in listeners:
                    listeners.remove(self)
                    listeners.sort(key=lambda obj: obj.priority.value)


def event_listener(event_class: type, priority: Priority = Priority.NORMAL) -> Callable:
    """
    Register event listener

    Args:
        event_class (type): the event
        priority (Priority): the priority of this listener
    """

    def registry(func) -> EventListener:
        listener = EventListener(func, event_class, priority)
        (event_listeners.setdefault(func.__module__, dict())
         .setdefault(event_class, []).append(listener))
        event_listeners[func.__module__][event_class].sort(key=lambda obj: obj.priority.value)
        return listener

    return registry


def unregister_listener(listener: Callable):
    """
    Unregister event listener

    Args:
        listener: the listener
    """
    warnings.warn("The unregister_listener() is deprecated", DeprecationWarning)
    assert isinstance(listener, EventListener), "the listener must be a registered listener"
    listener.unregister()


def unregister_module(module):
    """
    Unregister all listeners of a module

    Args:
        module: the module
    """
    event_listeners.pop(module)
