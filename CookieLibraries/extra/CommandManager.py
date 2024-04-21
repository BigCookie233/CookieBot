# coding: utf-8

# Created by BigCookie233

import inspect

from CookieLibraries.extra import MessageMatcher
from CookieLibraries.protocol import MessageUtils
from CookieLibraries.extra import Matchers
prefix = "/"


class CommandExecutor(MessageMatcher.MessageListener):
    def __init__(self, func, cmd):
        assert isinstance(cmd, str), "the command must be a str"
        self.cmd = cmd

        def matcher(event: MessageUtils.ReceiveGroupMessageEvent):
            text = Matchers.startswith(f"{prefix}{self.cmd}")(event)
            if text is not None:
                return text.split(" ")[1:]

        super().__init__(func, matcher)


def command_executor(cmd: str):
    def wrapper(func):
        executor_obj = CommandExecutor(func, cmd)
        executor_obj.register()
        return executor_obj

    return wrapper
