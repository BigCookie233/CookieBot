# coding: utf-8
# Created by BigCookie233
import warnings

import CookieLibraries.core.EventManager as EventManager
import CookieLibraries.core.PluginManager as PluginManager
from CookieLibraries.protocol.MessageUtils import ReceiveMessageEvent


def on_enable(func):
    warnings.warn("the on_enable() is deprecated", DeprecationWarning)
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def on_disable(func):
    warnings.warn("the on_disable() is deprecated", DeprecationWarning)
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)


def on_message(func):
    warnings.warn("the on_message() is deprecated", DeprecationWarning)
    return EventManager.event_listener(ReceiveMessageEvent)(func)
