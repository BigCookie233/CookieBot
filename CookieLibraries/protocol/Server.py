# coding: utf-8

# Created by BigCookie233

import logging

from flask import Flask, request
from werkzeug.serving import make_server

from CookieLibraries.core import ConfigManager
from CookieLibraries.core.DependencyInjector import autowired, get_instance
from CookieLibraries.protocol import MessageUtils, BotController

app = Flask("CookieBot")


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()

    if data['post_type'] == "message" and data['message_type'] == 'group':  # Group Message
        message = MessageUtils.ReceiveGroupMessageEvent(data['message'], data['message_id'],
                                                        BotController.GroupSender(data["sender"], data['group_id']))
        get_instance(logging.Logger).info("收到群 {} 内 {}({}) 的消息: {} ({})".format(
            message.sender.group_id, message.sender.nickname, message.sender.user_id, data['raw_message'],
            message.message_id))
        message.call()

    return "OK"


@autowired
def start(logger: logging.Logger):
    # 禁用werkzeug的日志记录
    logging.getLogger('werkzeug').disabled = True
    try:
        config = ConfigManager.GlobalConfig()
        logger.info(f"Starting server on {config.server_host}:{config.server_port}")
        server = make_server(config.server_host, config.server_port, app)
        server.serve_forever()
    except Exception as e:
        logger.error(f"Cannot start server: {e}")
    finally:
        logger.info("Stopping server")
