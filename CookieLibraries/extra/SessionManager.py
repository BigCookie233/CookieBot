# coding: utf-8

# Created by BigCookie233

from typing import Callable

from CookieLibraries.extra.MessageMatcher import MessageListener
from CookieLibraries.protocol import ReceiveGroupMessageEvent, Sender

_sessions = {}


class Trigger(MessageListener):
    def __init__(self, matcher):
        super().__init__(None, matcher)
        self.sender = None

    def on_sender(self, sender):
        self.sender = sender
        return self

    def __call__(self, event: ReceiveGroupMessageEvent):
        if event.sender.user_id == self.sender.user_id:
            super().__call__(event)


class Session:
    def __init__(self, creater):
        self.sender: Sender = None
        self.message = None
        self.trigger = None
        self.handler = None
        self.creater = creater

    def resume(self, sender, message):
        self.sender = sender
        self.message = message
        try:
            if self.trigger is not None:
                self.trigger.unregister()
            self.trigger = (next(self.handler)
                               .set_callback(lambda p1, p2: self.resume(p1, p2))
                               .on_sender(sender)
                               .register())
        except StopIteration:
            del _sessions[id(self.creater)][sender.user_id]


class SessionHandler(MessageListener):
    def __init__(self, callback: Callable, matcher):
        super().__init__(callback, matcher)
        super().on(ReceiveGroupMessageEvent)

    def __call__(self, event: ReceiveGroupMessageEvent):
        if event.sender.user_id not in _sessions.get(id(self), {}):
            session = Session(self)
            message = self.matcher(event)
            if message is not None:
                sender = event.sender
                session.handler = self.callback(session)
                _sessions.setdefault(id(self), {})[event.sender.user_id] = session
                session.resume(sender, message)


def session_handler(matcher):
    return lambda func: SessionHandler(func, matcher).register()
