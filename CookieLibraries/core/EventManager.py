# coding: utf-8

# Created by BigCookie233

import inspect
from enum import Enum
from typing import Callable

from CookieLibraries.core import LoggerUtils, Utils, ThreadPool

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
        ret = []
        for event_class, listeners in _event_listeners.items():
            if issubclass(self.__class__, event_class):
                ret.extend(listeners)
        ret.sort(key=lambda obj: obj.priority.value)
        return ret

    @ThreadPool.async_task
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
    def __init__(self, func: Callable, priority: Priority = Priority.NORMAL):
        assert (callable(func)
                and len(inspect.signature(func).parameters) == 1
                and hasattr(func, "__annotations__")), "invalid listener"
        event_class = next(iter(func.__annotations__.values()))
        assert isinstance(event_class, type) and issubclass(event_class, Event), "invalid event"
        assert isinstance(priority, Priority), "invalid priority"
        self.__func = func
        self.__event_class = event_class
        self.__priority = priority

    def __call__(self, event: Event):
        assert isinstance(event, self.__event_class), "invalid event"
        self.__func(event)

    def register(self):
        _event_listeners.setdefault(self.__event_class, []).append(self)
        return self

    def unregister(self):
        """
        Unregister the event listener
        """
        assert (self.__event_class in _event_listeners
                and self in _event_listeners[self.__event_class]), "the listener has not been registered yet"
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
        assert isinstance(priority, Priority), "invalid priority"
        self.__priority = priority

    @event_class.setter
    def event_class(self, event_class: type):
        assert isinstance(event_class, type) and issubclass(event_class, Event), "invalid event"
        self.unregister()
        self.__event_class = event_class
        self.register()


@Utils.allow_default
def event_listener(func, priority: Priority = Priority.NORMAL) -> EventListener:
    """
    Register event listener
    """
    return EventListener(func, priority).register()
