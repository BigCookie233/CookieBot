# coding:utf-8
#   __  __       ____       _         ____        _   _____
#  |  \/  |_   _|  _ \ __ _(_)_ __   | __ )  ___ | |_|___  \
#  | |\/| | | | | |_) / _` | | '_ \  |  _ \ / _ \| __| __) |
#  | |  | | |_| |  _ < (_| | | | | | | |_) | (_) | |_ / __/
#  |_|  |_|\__,_|_| \_\__,_|_|_| |_| |____/ \___/ \__|_____|
import atexit
import sys

from flask import Flask, request
from werkzeug.serving import make_server
import logging
import os

from CookieLibraries import *
from Lib import *

VERSION = "2.0.0-dev"  # 版本
VERSION_WEEK = "24W11A"  # 版本周

logger = None
app = Flask(__name__)

api = OnebotAPI.OnebotAPI()

request_list = []


# 结束运行
@atexit.register
def finalize_and_cleanup():
    # TODO: 清理缓存文件等
    logger.info("MuRainBot结束运行！\n")


# 上报
@app.route('/', methods=["POST"])
def post_data():
    data = request.get_json()
    if data in request_list:
        return "OK"
    request_list.append(data)

    if data['post_type'] == "message" and data['message_type'] == 'group':  # 如果是群聊信息
        username = data['sender']['nickname']  # 获取信息发送者的昵称
        if data['sender']['card'] != "":
            username = data['sender']['card']  # 若用户设置了群昵称则把用户名设为群昵称
        group_name = api.get("/get_group_info", {"group_id": data['group_id']})["group_name"]

        message = QQRichText.cq_decode(data['raw_message'])

        logger.info("收到群 %s(%s) 内 %s(%s) 的消息: %s (%s)" % (
            group_name, data['group_id'], username, data['sender']['user_id'], message,
            data['message_id']))

        # 加群邀请
        if data['post_type'] == 'request' and data['request_type'] == 'group':
            logger.info("收到来自%s的加群邀请, 群号%s, flag:%s, 类型: %s" %
                        (data['user_id'], data['group_id'], data['flag'], data['sub_type']))

        # 戳一戳
        if data['post_type'] == "notice" and data['notice_type'] == 'notify':
            logger.info("检测到群号为%s内，%s戳了戳%s" %
                        (data['group_id'], data['user_id'], data['target_id']))

        # 进群聊
        if data['post_type'] == "notice" and data['notice_type'] == "group_increase":
            logger.info("检测到群号为%s内，%s进群了，操作者%s" %
                        (data['group_id'], data['user_id'], data['operator_id']))

        # 退群聊
        if data['post_type'] == "notice" and data['notice_type'] == "group_decrease":
            type_ = data['sub_type']
            oid = data['operator_id']
            group_id = data['group_id']
            user_id = data['user_id']
            if type_ == "leave":
                logger.info("检测到%s退出了群聊%s" % (user_id, group_id))
            elif type_ == "kick":
                logger.info("检测到%s被%s踢出了群聊%s" % (user_id, oid, group_id))
            elif type_ == "kick_me" or user_id == bot_uid:
                logger.info("检测到Bot被%s踢出了群聊%s" % (oid, group_id))

    return "OK"


# 主函数
if __name__ == '__main__':
    data_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'data')

    LoggerManager.init("logs")
    logger = LoggerManager.logger
    logger.info(f"MuRain Bot开始运行，当前版本：{VERSION}({VERSION_WEEK})")

    def exit_if_error_occurred(exit_code = 0):
        if LoggerManager.last_error is not None:
            sys.exit(exit_code)

    config = Configs.GlobalConfig()
    exit_if_error_occurred(1)

    bot_uid = config.get_user_id()
    bot_name = config.get_nick_name()
    bot_admin = config.get_bot_admin()

    PluginManager.load_modules("plugins")
    exit_if_error_occurred(2)
    logger.info("插件导入完成，共成功导入 {} 个插件".format(len(PluginManager.modules)))

    # 设置API
    api.set_ip(config.get_api_host(), config.get_api_port())
    logger.info("调用API: {}".format(str(api)))

    # 检测bot名称与botUID是否为空或未设置
    if bot_uid is None or bot_name == "" or bot_uid == 123456 or bot_name is None:
        logger.warning("配置文件中未找到BotUID或昵称，将自动获取！")
        try:
            bot_info = api.get("/get_login_info")
            bot_uid, bot_name = bot_info["user_id"], bot_info["nickname"]
        except (TypeError, ConnectionRefusedError):
            logger.error("获取BotUID与昵称失败！")

    # 禁用werkzeug的日志记录
    logging.getLogger('werkzeug').disabled = True

    # 启动监听服务器
    try:
        logger.info("启动监听服务器: {}:{}".format(config.get_server_host(), config.get_server_port()))
        server = make_server(config.get_server_host(), config.get_server_port(), app)
        server.serve_forever()
    except:
        logger.error("监听服务器启动失败！")
    finally:
        logger.info("监听服务器结束运行！")
