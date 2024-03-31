# coding: utf-8

# Created by BigCookie233

from CookieLibraries import *

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "v1.0 SNAPSHOT"

logger = LoggerManager.logger


@Events.on_group_message
def on_message(event: Events.ReceiveGroupMessageEvent):
    msg = event.message
    if msg.startswith_atme() and msg.segment_chain[1] == " ping!":
        MessageManager.Message().at(msg.sender["user_id"]).text(" pong!").send_to_group(msg.group_id)
