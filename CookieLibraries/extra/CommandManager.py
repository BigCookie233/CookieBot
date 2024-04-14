# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.core import EventManager
from CookieLibraries.protocol import MessageUtils

_command_executors = {}
prefix = "/"


def command(cmd: str):
    assert isinstance(cmd, str), "the command must be a str"

    def wrapper(func):
        params_len = len(inspect.signature(func).parameters)
        assert params_len == 3, f"the listener takes {params_len} positional arguments but 3 and only 3 will be given"
        _command_executors[cmd] = func
        return func

    return wrapper


@EventManager.event_listener
def message_listener(event: MessageUtils.ReceiveGroupMessageEvent):
    if event.segment_chain and isinstance(event.segment_chain[0], MessageUtils.TextSegment):
        if event.segment_chain[0].text.startswith(prefix):
            cmd = event.segment_chain[0].text[1:].split(" ")
            _command_executors[cmd[0]](event.sender, event.group_id, cmd[1:])
