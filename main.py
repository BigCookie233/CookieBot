# coding:utf-8
import logging
import os

import atexit
import requests
from flask import Flask, request
from werkzeug.serving import make_server

from CookieLibraries import *

VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24W11A"  # 版本周

logger = None
app = Flask("CookieBot")


# 结束运行
@atexit.register
def finalize_and_cleanup():
    ThreadPool.thread_pool.shutdown()
    logger.info("MuRainBot结束运行！\n")


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()

    if data['post_type'] == "message" and data['message_type'] == 'group':  # 如果是群聊信息
        username = data['sender']['nickname']  # 获取信息发送者的昵称
        if data['sender']['card'] != "":
            username = data['sender']['card']  # 若用户设置了群昵称则把用户名设为群昵称
        # group_name = api.get("/get_group_info", {"group_id": data['group_id']})["group_name"]
        # message = QQRichText.cq_decode(data['raw_message'])
        message = MessageManager.ReceivedGroupMessage(data['message'], data['message_id'], data['sender'],
                                                      data['group_id'])

        logger.info("收到群 {} 内 {}({}) 的消息: {} ({})".format(
            message.group_id, message.sender["nickname"], message.sender['user_id'], data['raw_message'],
            message.message_id))
        Events.ReceiveGroupMessageEvent(message).call()

        # # 加群邀请
        # if data['post_type'] == 'request' and data['request_type'] == 'group':
        #     logger.info("收到来自%s的加群邀请, 群号%s, flag:%s, 类型: %s" %
        #                 (data['user_id'], data['group_id'], data['flag'], data['sub_type']))
        #
        # # 戳一戳
        # if data['post_type'] == "notice" and data['notice_type'] == 'notify':
        #     logger.info("检测到群号为%s内，%s戳了戳%s" %
        #                 (data['group_id'], data['user_id'], data['target_id']))
        #
        # # 进群聊
        # if data['post_type'] == "notice" and data['notice_type'] == "group_increase":
        #     logger.info("检测到群号为%s内，%s进群了，操作者%s" %
        #                 (data['group_id'], data['user_id'], data['operator_id']))
        #
        # # 退群聊
        # if data['post_type'] == "notice" and data['notice_type'] == "group_decrease":
        #     type_ = data['sub_type']
        #     oid = data['operator_id']
        #     group_id = data['group_id']
        #     user_id = data['user_id']
        #     if type_ == "leave":
        #         logger.info("检测到%s退出了群聊%s" % (user_id, group_id))
        #     elif type_ == "kick":
        #         logger.info("检测到%s被%s踢出了群聊%s" % (user_id, oid, group_id))
        #     elif type_ == "kick_me" or user_id == bot_uid:
        #         logger.info("检测到Bot被%s踢出了群聊%s" % (oid, group_id))

    return "OK"


# 主函数
if __name__ == '__main__':
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

    LoggerManager.init("logs")
    logger = LoggerManager.logger
    logger.info(f"MuRain Bot开始运行，当前版本：{VERSION}({VERSION_WEEK})")

    Configs.global_config = Configs.GlobalConfig()
    config = Configs.global_config

    PluginManager.load_plugins("plugins")
    logger.info("插件导入完成，共成功导入 {} 个插件".format(len(PluginManager.plugins)))

    BotController.init()
    ThreadPool.init()

    bot_info = BotController.send_get_request("get_login_info")
    if bot_info is None:
        logger.error("获取BotUID与昵称失败！")
    bot_uid, bot_name = bot_info["user_id"], bot_info["nickname"]

    # 禁用werkzeug的日志记录
    logging.getLogger('werkzeug').disabled = True

    # 启动监听服务器
    try:
        logger.info("启动监听服务器: {}:{}".format(config.server_host, config.server_port))
        server = make_server(config.server_host, config.server_port, app)
        server.serve_forever()
    except:
        logger.error("监听服务器启动失败！")
    finally:
        logger.info("监听服务器结束运行！")
