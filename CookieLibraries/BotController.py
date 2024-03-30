# coding: utf-8

# Created by BigCookie233

import requests

import CookieLibraries.Configs as Configs
import CookieLibraries.LoggerManager as LoggerManager

base_url = None


def init():
    global base_url
    config = Configs.GlobalConfig()
    base_url = "http://{}:{}/".format(config.api_host, config.api_port)


@LoggerManager.log_exception(True)
def send_request(node: str, json):
    if isinstance(base_url, str):
        response = requests.post(base_url + node, json=json)
        return response.json()["data"]


def send_group_message(group_id, message):
    send_request("send_group_msg", {"group_id": group_id, "message": message})
