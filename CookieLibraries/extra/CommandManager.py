# coding: utf-8
# Created by BigCookie233
from CookieLibraries.extra import Matchers
from CookieLibraries.extra import MessageMatcher
from CookieLibraries.protocol import ReceiveGroupMessageEvent

prefix = "/"


class CommandExecutor(MessageMatcher.MessageListener):
    def __init__(self, callback, cmd):
        assert isinstance(cmd, str), "the command must be a str"
        self.cmd = cmd

        def matcher(event: ReceiveGroupMessageEvent):
            text = Matchers.startswith(f"{prefix}{self.cmd}")(event)
            if text is not None:
                return text.split(" ")[1:]

        super().__init__(callback, matcher)


def command_executor(cmd: str):
    def wrapper(func):
        return CommandExecutor(func, cmd).on(ReceiveGroupMessageEvent).register()

    return wrapper
