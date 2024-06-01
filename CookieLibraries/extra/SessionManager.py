# coding: utf-8

# Created by BigCookie233

from typing import Callable

from CookieLibraries.extra.MessageMatcher import MessageListener
from CookieLibraries.protocol import ReceiveGroupMessageEvent, Sender

_sessions = {}


class Trigger(MessageListener):
    def __init__(self, matcher):
        super().__init__(None, matcher)


class Session:
    def __init__(self):
        self.sender: Sender = None
        self.message = None
        self.trigger = None
        self.handler = None


class SessionHandler(MessageListener):
    def __init__(self, callback: Callable, matcher):
        super().__init__(callback, matcher)
        super().on(ReceiveGroupMessageEvent)

    def __call__(self, event: ReceiveGroupMessageEvent):
        if event.sender.user_id not in _sessions.get(id(self), {}):
            session = Session()
            session.message = self.matcher(event)
            if session.message is not None:
                session.sender = event.sender
                session.handler = self.callback(session)
                try:
                    def func(sender, message):
                        _session: Session = _sessions[id(self)][sender.user_id]
                        _session.sender = sender
                        _session.message = message
                        try:
                            _session.trigger.unregister()
                            _session.trigger = next(_session.handler).set_callback(func).register()
                        except StopIteration:
                            del _sessions[id(self)][sender.user_id]
                    session.trigger = next(session.handler).set_callback(func).register()
                    _sessions.setdefault(id(self), {})[event.sender.user_id] = session
                except StopIteration:
                    del _sessions[id(self)][event.sender.user_id]




def session_handler(matcher):
    return lambda func: SessionHandler(func, matcher).register()
