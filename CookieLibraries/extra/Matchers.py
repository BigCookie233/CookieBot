# coding: utf-8

# Created by BigCookie233

from CookieLibraries.protocol import MessageUtils


def text_msg(event: MessageUtils.ReceiveGroupMessageEvent) -> str:
    if len(event.segment_chain) == 1 and isinstance(event.segment_chain[0], MessageUtils.TextSegment):
        return event.segment_chain[0].text


def equals(keyword: str):
    def matcher(event: MessageUtils.ReceiveGroupMessageEvent) -> str:
        text = text_msg(event)
        if text is not None and text == keyword:
            return text

    return matcher


def startswith(keyword: str):
    def matcher(event: MessageUtils.ReceiveGroupMessageEvent) -> str:
        text = text_msg(event)
        if text is not None and text.startswith(keyword):
            return text

    return matcher


def endswith(keyword: str):
    def matcher(event: MessageUtils.ReceiveGroupMessageEvent) -> str:
        text = text_msg(event)
        if text is not None and text.endswith(keyword):
            return text

    return matcher
