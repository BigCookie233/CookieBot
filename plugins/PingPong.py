# coding: utf-8

# Created by BigCookie233

from CookieLibraries.core import *
from CookieLibraries.extra import *
from CookieLibraries.protocol import *

PLUGIN_NAME = "PingPong"
PLUGIN_VERSION = "1.0-SNAPSHOT"


@command_executor("ping")
def on_message(sender: Sender, params: list):
    sender.reply(MessageBuilder().at(sender.user_id).text(" pong!"))
