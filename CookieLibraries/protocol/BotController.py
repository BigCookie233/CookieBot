# coding: utf-8
# Created by BigCookie233
import importlib

import requests

from ..core import EventManager, LoggerUtils, ThreadPool, Cacher
from .MessageUtils import Message


base_url = None


def init():
    global base_url
    config = importlib.import_module(name="CookieLibraries.core.ConfigManager").GlobalConfig()
    base_url = f"http://{config.api_host}:{config.api_port}/"


@ThreadPool.async_task
@LoggerUtils.log_exception(True)
def send_post_request(node: str, json):
    if isinstance(base_url, str):
        response = requests.post(base_url + node, json=json)
        return response.json()["data"]


@LoggerUtils.log_exception(True)
def send_get_request(node: str):
    if isinstance(base_url, str):
        response = requests.get(base_url + node)
        return response.json()["data"]


# TODO: 重构信息获取
@Cacher.cache
def get_login_info():
    return send_get_request("get_login_info")


class Sender:
    def __init__(self, data: dict):
        self.user_id = data.get("user_id")
        self.nickname = data.get("nickname")
        self.sex = data.get("sex")
        self.age = data.get("age")

    def reply(self, message: Message):
        pass


class GroupSender(Sender):
    def __init__(self, data: dict, group_id):
        super().__init__(data)
        self.card = data.get("card")
        self.area = data.get("area")
        self.level = data.get("level")
        self.role = data.get("role")
        self.title = data.get("title")
        self.group_id = group_id

    def reply(self, message: Message):
        message.send_to_group(self.group_id)


class SendActionEvent(EventManager.CancellableEvent):
    def __init__(self, action):
        super().__init__()
        self.action = action

    def call(self):
        super().call()
        send_post_request(self.action, self.data)

    @property
    def data(self) -> dict:
        pass


class SendGroupMessageEvent(SendActionEvent):
    def __init__(self, message, group_id):
        super().__init__("send_group_msg")
        self.message = message
        self.group_id = group_id

    @property
    def data(self) -> dict:
        return {"group_id": self.group_id, "message": self.message}
