# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.core import EventManager
from CookieLibraries.protocol import MessageUtils


class MessageListener(EventManager.EventListener):
    def __init__(self, func, matcher):
        assert callable(matcher), "the matcher must be a callable object"
        params_len = len(inspect.signature(func).parameters)
        assert params_len == 3, f"the listener takes {params_len} positional arguments but 3 and only 3 will be given"
        self.matcher = matcher

        def call_func(event: MessageUtils.ReceiveGroupMessageEvent):
            matched_message = self.matcher(event)
            if matched_message is not None:
                func(event.sender, event.group_id, matched_message)

        super().__init__(call_func)


def match_message(matcher):
    return lambda func: MessageListener(func, matcher).register()
