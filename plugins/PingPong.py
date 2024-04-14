# coding: utf-8

# Created by BigCookie233

from CookieLibraries.core import *
from CookieLibraries.protocol import *

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "1.0-SNAPSHOT"

logger = LoggerUtils.logger


@EventManager.event_listener
def on_message(event: MessageUtils.ReceiveGroupMessageEvent):
    if event.startswith_atme() and event.segment_chain[1] == " ping!":
        MessageUtils.MessageBuilder().at(event.sender.user_id).text(" pong!").send_to_group(event.group_id)
