# coding: utf-8

# Created by BigCookie233

import CookieLibraries.EventManager as EventManager
import CookieLibraries.PluginManager as PluginManager


class ReceiveMessageEvent(EventManager.Event):
    def __init__(self, message):
        super().__init__()
        self.message = message


class ReceiveGroupMessageEvent(ReceiveMessageEvent):
    def __init__(self, message):
        super().__init__(message)


class SendActionEvent(EventManager.CancellableEvent):
    def __init__(self, action):
        super().__init__()
        self.action = action

    @property
    def data(self) -> dict:
        return {}


class SendGroupMessageEventSend(SendActionEvent):
    def __init__(self, message, group_id):
        super().__init__("send_group_msg")
        self.message = message
        self.group_id = group_id

    @property
    def data(self) -> dict:
        return {"group_id": self.group_id, "message": self.message}


def on_enable(func):
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def on_disable(func):
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)


def on_message(func):
    return EventManager.event_listener(ReceiveMessageEvent)(func)


def on_group_message(func):
    return EventManager.event_listener(ReceiveGroupMessageEvent)(func)


def on_group_message_send(func):
    return EventManager.event_listener(SendGroupMessageEventSend)(func)
