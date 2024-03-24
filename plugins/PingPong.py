# coding: utf-8

# Created by BigCookie233

import CookieLibraries

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "v0.1 SNAPSHOT"

logger = CookieLibraries.LoggerManager.logger


@CookieLibraries.Events.on_group_message
def on_message(event: CookieLibraries.Events.ReceiveGroupMessageEvent):
    if event.message.raw_message == "[CQ:at,qq=629596434] ping":
        CookieLibraries.MessageManager.Message("pong!").send_to_group(event.message.group_id)
