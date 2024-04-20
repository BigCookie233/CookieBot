# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.core import EventManager
from CookieLibraries.protocol import MessageUtils


class KeywordListener(EventManager.EventListener):
    def __init__(self, func, matcher):
        assert callable(matcher), "the matcher must be a callable object"
        params_len = len(inspect.signature(func).parameters)
        assert params_len == 3, f"the listener takes {params_len} positional arguments but 3 and only 3 will be given"
        self.matcher = matcher

        def call_func(event: MessageUtils.ReceiveGroupMessageEvent):
            keyword = self.matcher(event)
            if keyword is not None:
                func(event.sender, event.group_id, keyword)

        super().__init__(call_func, MessageUtils.ReceiveGroupMessageEvent)


def keyword_listener(matcher):
    def wrapper(func):
        listener_obj = KeywordListener(func, matcher)
        listener_obj.register()
        return listener_obj

    return wrapper
