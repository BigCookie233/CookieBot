# coding: utf-8

# Created by BigCookie233

import requests
import importlib

import CookieLibraries.Configs as Configs
import CookieLibraries.EventManager as EventManager
import CookieLibraries.Events as Events
import CookieLibraries.LoggerManager as LoggerManager
import CookieLibraries.ThreadPool as ThreadPool

base_url = None


def init():
    global base_url
    config = importlib.import_module(name="CookieLibraries.Configs").GlobalConfig()
    base_url = "http://{}:{}/".format(config.api_host, config.api_port)


@ThreadPool.async_task
@LoggerManager.log_exception(True)
def send_post_request(node: str, json):
    if isinstance(base_url, str):
        response = requests.post(base_url + node, json=json)
        return response.json()["data"]


def send_get_request(node: str):
    if isinstance(base_url, str):
        response = requests.get(base_url + node)
        return response.json()["data"]


@EventManager.event_listener(Events.SendActionEvent, EventManager.Priority.LOWEST)
def group_message_sender(event: Events.SendActionEvent):
    send_post_request(event.action, event.data)
