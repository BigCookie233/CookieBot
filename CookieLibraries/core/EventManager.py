# coding: utf-8
# Created by BigCookie233
from enum import Enum
from threading import RLock

from .LoggerUtils import traceback_exception
from .ThreadPool import async_task

_event_listeners = {}


class Priority(Enum):
    HIGHEST = 0
    HIGH = 1
    NORMAL = 2
    LOW = 3
    LOWEST = 4


class HookStage(Enum):
    PRE = 0
    POST = 1


_hooks = {
    HookStage.PRE: [],
    HookStage.POST: []
}


class Event:
    """
    Event base class
    """

    def __init__(self):
        self.__dispatch_lock = RLock()
        self.__skipped = False

    @property
    def listeners(self):
        ret = []
        for event_class, listeners in _event_listeners.items():
            if issubclass(self.__class__, event_class):
                ret.extend(listeners)
        ret.sort(key=lambda obj: obj.priority.value)
        return ret

    def skip_dispatch(self):
        with self.__dispatch_lock:
            self.__skipped = True

    @async_task
    @traceback_exception
    def call(self):
        """
        Call event
        """
        with self.__dispatch_lock:
            for listener in self.listeners:
                self.__skipped = False
                for hook_listener in _hooks[HookStage.PRE]:
                    hook_listener(self, listener)
                if not self.__skipped:
                    listener(self)
                for hook_listener in _hooks[HookStage.POST]:
                    hook_listener(self, listener)


class CancellableEvent(Event):
    """
    Cancellable event base class
    """

    def __init__(self):
        super().__init__()
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
    def __init__(self, callback, event: type, prio: Priority = Priority.NORMAL):
        self.callback = traceback_exception(callback)
        assert isinstance(event, type) and issubclass(event, Event), "invalid event"
        self.__event = event
        self.__priority = prio

    def __call__(self, event: Event):
        return self.callback(event)

    def set_priority(self, prio: Priority):
        assert isinstance(prio, Priority), "invalid priority"
        self.__priority = prio

    def register(self):
        _event_listeners.setdefault(self.__event, []).append(self)
        return self

    def unregister(self):
        """
        Unregister the event listener
        """
        assert (self.__event in _event_listeners
                and self in _event_listeners[self.__event]), "the listener has not been registered yet"
        _event_listeners[self.__event].remove(self)
        if not _event_listeners[self.__event]:
            _event_listeners.pop(self.__event)

    @property
    def priority(self) -> Priority:
        return self.__priority

    @property
    def event(self) -> type:
        return self.__event


def event_listener(func) -> EventListener:
    """
    Register event listener
    """
    event = next(iter(func.__annotations__.values()))
    return EventListener(func, event).register()


def priority(prio: Priority):
    def wrapper(listener: EventListener):
        assert isinstance(listener, EventListener), "invalid listener"
        listener.set_priority(prio)
        return listener

    return wrapper


def hook(stage: HookStage):
    assert isinstance(stage, HookStage), "invalid stage"

    def wrapper(func):
        _hooks[stage].append(func)
        return func

    return wrapper
