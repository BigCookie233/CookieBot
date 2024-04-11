# coding: utf-8

# Created by BigCookie233

from CookieLibraries.core import *
from CookieLibraries.extra import *

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "1.0-SNAPSHOT"

logger = LoggerUtils.logger


@Events.on_group_message
def on_message(event: CookieLibraries.core.MessageUtils.ReceiveGroupMessageEvent):
    msg = event.message
    if msg.startswith_atme() and msg.segment_chain[1] == " ping!":
        MessageUtils.Message().at(msg.sender["user_id"]).text(" pong!").send_to_group(msg.group_id)
