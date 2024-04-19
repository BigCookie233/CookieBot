# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.core import EventManager
from CookieLibraries.protocol import MessageUtils

prefix = "/"


class CommandExecutor(EventManager.EventListener):
    def __init__(self, func, cmd):
        assert isinstance(cmd, str), "the command must be a str"
        params_len = len(inspect.signature(func).parameters)
        assert params_len == 3, f"the listener takes {params_len} positional arguments but 3 and only 3 will be given"
        self.cmd = cmd

        def call_func(event: MessageUtils.ReceiveGroupMessageEvent):
            if len(event.segment_chain) == 1 and isinstance(event.segment_chain[0], MessageUtils.TextSegment):
                if event.segment_chain[0].text.startswith(f"{prefix}{self.cmd}"):
                    func(event.sender, event.group_id, event.segment_chain[0].text.split(" ")[1:])

        super().__init__(call_func, MessageUtils.ReceiveGroupMessageEvent)


def command_executor(cmd: str):
    def wrapper(func):
        executor_obj = CommandExecutor(func, cmd)
        executor_obj.register()
        return executor_obj

    return wrapper
