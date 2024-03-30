# coding: utf-8

# Created by BigCookie233

import CookieLibraries

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "v0.1 SNAPSHOT"

logger = CookieLibraries.LoggerManager.logger


@CookieLibraries.Events.on_group_message
def on_message(event: CookieLibraries.Events.ReceiveGroupMessageEvent):
    msg = event.message
    if msg.segment_chain[0] == "ping!":
        CookieLibraries.MessageManager.Message().at(msg.sender["user_id"]).text(" pong!").send_to_group(msg.group_id)
