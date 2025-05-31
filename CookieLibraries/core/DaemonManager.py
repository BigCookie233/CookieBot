# coding: utf-8
# Created by BigCookie233
import threading

from .Bootstrap import bootstrap
from .LoggerUtils import traceback_exception

_daemons = []


def daemon(func):
    thread = threading.Thread(target=traceback_exception(func))
    thread.daemon = True
    _daemons.append(thread)
    return func


@bootstrap
def start():
    for thread in _daemons:
        thread.start()
