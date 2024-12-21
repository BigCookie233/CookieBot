# coding: utf-8
# Created by BigCookie233
from enum import Enum
from threading import RLock

from .LoggerUtils import traceback_exception
from .ThreadPool import async_task
from .Utils import allow_default

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
    def __init__(self):
        self.callback = None
        self.__event = None
        self.__priority = Priority.NORMAL

    def __call__(self, event: Event):
        return self.callback(event)

    def on(self, event: type):
        assert isinstance(event, type) and issubclass(event, Event), "invalid event"
        self.__event = event
        return self

    def set_priority(self, priority: Priority):
        assert isinstance(priority, Priority), "invalid priority"
        self.__priority = priority
        return self

    def set_callback(self, callback):
        self.callback = traceback_exception(callback)
        return self

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


@allow_default
def event_listener(func, priority: Priority = Priority.NORMAL) -> EventListener:
    """
    Register event listener
    """
    event = next(iter(func.__annotations__.values()))
    return EventListener().set_callback(func).on(event).set_priority(priority).register()


def hook(stage: HookStage):
    assert isinstance(stage, HookStage), "invalid stage"

    def wrapper(func):
        _hooks[stage].append(func)
        return func

    return wrapper
