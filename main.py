# coding:utf-8
import logging

from flask import Flask, request
from werkzeug.serving import make_server

from CookieLibraries import *

VERSION = "2.1.0-dev"
app = Flask("CookieBot")


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()

    if data['post_type'] == "message" and data['message_type'] == 'group':  # Group Message
        message = MessageManager.ReceivedGroupMessage(data['message'], data['message_id'], data['sender'],
                                                      data['group_id'])
        logger.info("收到群 {} 内 {}({}) 的消息: {} ({})".format(
            message.group_id, message.sender["nickname"], message.sender['user_id'], data['raw_message'],
            message.message_id))
        Events.ReceiveGroupMessageEvent(message).call()

    return "OK"


# 主函数
if __name__ == '__main__':
    # Initialize Logger
    print("Initializing Logger")
    LoggerManager.init("logs")
    # Start up
    logger = LoggerManager.logger
    logger.info("Starting up CookieBot {}".format(VERSION))
    # Load Config
    Configs.global_config = Configs.GlobalConfig()
    config = Configs.global_config
    # Load Plugins
    logger.info("Loading plugins...")
    PluginManager.load_plugins("plugins")
    logger.info("Loaded {} plugins".format(len(PluginManager.plugins)))
    # Initialize Controller
    BotController.init()
    # Initialize Thread Pool
    logger.info("Initializing Thread Pool")
    ThreadPool.init()
    # Get Profile
    bot_info = BotController.send_get_request("get_login_info")
    if bot_info is None:
        logger.error("获取BotUID与昵称失败！")
    Configs.bot_profile = (bot_info["user_id"], bot_info["nickname"])
    # 禁用werkzeug的日志记录
    logging.getLogger('werkzeug').disabled = True
    # Start Server
    try:
        logger.info("Starting server on {}:{}".format(config.server_host, config.server_port))
        server = make_server(config.server_host, config.server_port, app)
        server.serve_forever()
    except Exception as e:
        logger.error("Cannot start server: {}".format(e))
    finally:
        logger.info("Closing Thread Pool")
        ThreadPool.thread_pool.shutdown()
        logger.info("Goodbye!")
