# coding: utf-8

# Created by BigCookie233

import inspect
import warnings
from enum import Enum
from typing import Callable

from CookieLibraries.core import LoggerUtils, Utils

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
            LoggerUtils.traceback_exception(listener)(self)


class CancellableEvent(Event):
    """
    Cancellable event base class
    """

    def __init__(self):
        self.__is_cancelled = False

    def cancel(self):
        """
        Cancel event
        """
        self.__is_cancelled = True

    @property
    def listeners(self):
        for listener in super().listeners:
            yield listener
            if self.__is_cancelled:
                break


class EventListener:
    def __init__(self, func: Callable, event_class: type, priority: Priority = Priority.NORMAL):
        assert callable(func), "the listener must be a callable object"
        params_len = len(inspect.signature(func).parameters)
        assert params_len == 1, f"the listener takes {params_len} positional arguments but 1 and only 1 will be given"
        assert isinstance(event_class, type) and issubclass(event_class, Event), "the event_class must be a event class"
        assert isinstance(priority, Priority), "the priority must be a priority"
        self.__func = func
        self.__event_class = event_class
        self.__priority = priority
        self.register()

    def __call__(self, event: Event):
        assert isinstance(event, self.__event_class), "invalid event for this listener"
        self.__func(event)

    def register(self):
        _event_listeners.setdefault(self.__event_class, []).append(self)
        _event_listeners[self.__event_class].sort(key=lambda obj: obj.priority.value)

    def unregister(self):
        """
        Unregister the event listener
        """
        _event_listeners[self.__event_class].remove(self)
        if not _event_listeners[self.__event_class]:
            _event_listeners.pop(self.__event_class)

    @property
    def func(self):
        return self.__func

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
        self.unregister()
        self.__event_class = event_class
        self.register()


@Utils.allow_default
def event_listener(func, event_class=None, priority=None) -> EventListener:
    """
    Register event listener
    """
    if isinstance(event_class, Priority) and priority is None:
        priority = event_class
        event_class = None
    if priority is None:
        priority = Priority.NORMAL
    if event_class is None and hasattr(func, "__annotations__"):
        event_class = next(iter(func.__annotations__.values()))
    return EventListener(func, event_class, priority)


def unregister_listener(listener: Callable):
    """
    Unregister event listener

    Args:
        listener: the listener
    """
    warnings.warn("the unregister_listener() is deprecated", DeprecationWarning)
    assert isinstance(listener, EventListener), "the listener must be a registered listener"
    listener.unregister()
