# coding: utf-8
# Created by BigCookie233
import json

from CookieLibraries.core import Cacher
from CookieLibraries.protocol import MessageUtils, BotController


class LongMessage(MessageUtils.Message):
    def __init__(self, msg_id):
        class LongMsgSegment(MessageUtils.MessageSegment):
            def __init__(self, msg_id_):
                self.msg_id = msg_id_
                super().__init__("longmsg")

            @property
            def data(self) -> dict:
                return {"id": str(self.msg_id)}

        super().__init__([LongMsgSegment(msg_id)])


class MarkdownMessage(LongMessage):
    def __init__(self, content):
        super().__init__(get_markdown_long_msg_id(json.dumps({"content": content})))


@Cacher.cache
def get_markdown_long_msg_id(data):
    return BotController.send_post_request("send_forward_msg", {
        "messages": [{
            "type": "node",
            "data": {
                "name": "假兔子",
                "uin": "10000",
                "content": [{
                    "type": "markdown",
                    "data": {
                        "content": data
                    }
                }]
            }
        }]
    }).result()
