# coding: utf-8
# Created by BigCookie233
import threading

from .EventManager import event_listener
from .LoggerUtils import traceback_exception
from .PluginManager import PostLoadPluginsEvent

_daemons = []


def daemon(func):
    thread = threading.Thread(target=traceback_exception(func))
    thread.daemon = True
    _daemons.append(thread)
    return func


@event_listener
def start(event: PostLoadPluginsEvent):
    for thread in _daemons:
        thread.start()
