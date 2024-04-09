# coding: utf-8

# Created by BigCookie233

import CookieLibraries.core.EventManager as EventManager
import CookieLibraries.core.PluginManager as PluginManager
from CookieLibraries.core.MessageUtils import ReceiveMessageEvent, ReceiveGroupMessageEvent, SendGroupMessageEvent


def on_enable(func):
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def on_disable(func):
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)


def on_message(func):
    return EventManager.event_listener(ReceiveMessageEvent)(func)


def on_group_message(func) -> EventManager.EventListener:
    return EventManager.event_listener(ReceiveGroupMessageEvent)(func)


def on_group_message_send(func):
    return EventManager.event_listener(SendGroupMessageEvent)(func)
