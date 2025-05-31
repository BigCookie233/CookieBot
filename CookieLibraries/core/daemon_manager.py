# coding: utf-8
# Created by BigCookie233
import threading

from .bootstrap import initializer
from .logger import traceback_exception

_daemons = []


def daemon(func):
    thread = threading.Thread(target=traceback_exception(func))
    thread.daemon = True
    _daemons.append(thread)
    return func


@initializer
def start():
    for thread in _daemons:
        thread.start()
