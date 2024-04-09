# coding: utf-8

# Created by BigCookie233

import importlib

import requests

from CookieLibraries.core import EventManager
from CookieLibraries.core import LoggerUtils
from CookieLibraries.core import ThreadPool

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


class SendActionEvent(EventManager.CancellableEvent):
    def __init__(self, action):
        super().__init__()
        self.action = action

    @property
    def data(self) -> dict:
        return {}


@EventManager.event_listener(SendActionEvent, EventManager.Priority.LOWEST)
def group_message_sender(event: SendActionEvent):
    send_post_request(event.action, event.data)
