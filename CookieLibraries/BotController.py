# coding: utf-8

# Created by BigCookie233

import requests

import CookieLibraries.Configs as Configs
import CookieLibraries.Events as Events
import CookieLibraries.LoggerManager as LoggerManager
import CookieLibraries.EventManager as EventManager
import CookieLibraries.ThreadPool as ThreadPool

base_url = None


def init():
    global base_url
    config = Configs.global_config
    base_url = "http://{}:{}/".format(config.api_host, config.api_port)


@ThreadPool.async_task
@LoggerManager.log_exception(True)
def send_request(node: str, json):
    if isinstance(base_url, str):
        response = requests.post(base_url + node, json=json)
        return response.json()["data"]


@EventManager.event_listener(Events.SendGroupMessageEvent, EventManager.Priority.LOWEST)
def group_message_sender(event: Events.SendGroupMessageEvent):
    send_request("send_group_msg", {"group_id": event.group_id, "message": event.message})
