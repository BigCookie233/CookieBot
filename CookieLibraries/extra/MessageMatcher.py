# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.core import EventManager
from CookieLibraries.protocol import ReceiveGroupMessageEvent


class MessageListener(EventManager.EventListener):
    def __init__(self, callback, matcher):
        self.matcher = matcher
        super().set_callback(callback)
        super().on(ReceiveGroupMessageEvent)

    def __call__(self, event: ReceiveGroupMessageEvent):
        matched_message = self.matcher(event)
        if matched_message is not None:
            self.callback(event.sender, matched_message)


def match_message(matcher):
    return lambda func: MessageListener(func, matcher).register()
