# coding: utf-8

# Created by BigCookie233

import CookieLibraries.EventManager as EventManager
import CookieLibraries.PluginManager as PluginManager


class ReceiveMessageEvent(EventManager.Event):
    def __init__(self, message):
        super().__init__()
        self.message = message


class SendMessageEvent(EventManager.Event):
    def __init__(self, message):
        super().__init__()
        self.message = message


class ReceiveGroupMessageEvent(ReceiveMessageEvent):
    def __init__(self, message):
        super().__init__(message)


class SendGroupMessageEvent(EventManager.Event):
    def __init__(self, message, group_id):
        super().__init__()
        self.message = message
        self.group_id = group_id


def on_enable(func):
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def on_disable(func):
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)


def on_message(func):
    return EventManager.event_listener(ReceiveMessageEvent)(func)


def on_message_send(func):
    return EventManager.event_listener(SendMessageEvent)(func)


def on_group_message(func):
    return EventManager.event_listener(ReceiveGroupMessageEvent)(func)


def on_group_message_send(func):
    return EventManager.event_listener(SendGroupMessageEvent)(func)
