# coding: utf-8

# Created by BigCookie233

import inspect
import warnings
from enum import Enum
from typing import Callable

from CookieLibraries.core import LoggerUtils

_event_listeners = {}


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

    @property
    def listeners(self):
        for event_class, listeners in _event_listeners.items():
            if issubclass(self.__class__, event_class):
                for listener in listeners:
                    yield listener

    def call(self):
        """
        Call event
        """
        for listener in self.listeners:
            LoggerUtils.traceback_exception(True)(listener)(self)


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
        for listener in self.listeners:
            LoggerUtils.traceback_exception(True)(listener)(self)
            if self.isCancelled:
                return None


class EventListener:
    def __init__(self, listener: Callable, event_class: type, priority: Priority):
        assert callable(listener), "the listener must be a callable object"
        params_len = len(inspect.signature(listener).parameters)
        assert params_len == 1, f"the listener takes {params_len} positional arguments but 1 and only 1 will be given"
        assert isinstance(event_class, type) and issubclass(event_class, Event), "the event_class must be a event class"
        assert isinstance(priority, Priority), "the priority must be a priority"
        self.__listener = listener
        self.__event_class = event_class
        self.__priority = priority
        _event_listeners.setdefault(self.__event_class, []).append(self)
        _event_listeners[self.__event_class].sort(key=lambda obj: obj.priority.value)

    @property
    def listener(self):
        return self.__listener

    @property
    def priority(self) -> Priority:
        return self.__priority

    @property
    def event_class(self) -> type:
        return self.__event_class

    @priority.setter
    def priority(self, priority: Priority):
        assert isinstance(priority, Priority), "the priority must be a priority"
        self.__priority = priority
        _event_listeners[self.__event_class].sort(key=lambda obj: obj.priority.value)

    @event_class.setter
    def event_class(self, event_class: type):
        assert isinstance(event_class, type) and issubclass(event_class, Event), "the event_class must be a event class"
        _event_listeners[self.__event_class].remove(self)
        self.__event_class = event_class
        _event_listeners.setdefault(self.__event_class, []).append(self)
        _event_listeners[self.__event_class].sort(key=lambda obj: obj.priority.value)

    def __call__(self, event: Event):
        assert isinstance(event, self.__event_class), "invalid event for this listener"
        self.__listener(event)

    def unregister(self):
        """
        Unregister the event listener
        """
        _event_listeners[self.__event_class].remove(self)


def event_listener(event_class: type, priority: Priority = Priority.NORMAL) -> Callable:
    """
    Register event listener

    Args:
        event_class (type): the event
        priority (Priority): the priority of this listener
    """

    def registry(func) -> EventListener:
        listener = EventListener(func, event_class, priority)
        _event_listeners.setdefault(event_class, []).append(listener)
        _event_listeners[event_class].sort(key=lambda obj: obj.priority.value)
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
    warnings.warn("The unregister_module() is deprecated", DeprecationWarning)
