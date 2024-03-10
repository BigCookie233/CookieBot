# coding: utf-8

# Created by BigCookie233

import CookieLibraries.ConfigManager as ConfigManager


class GlobalConfig(ConfigManager.Config):
    def __init__(self):
        super().__init__("config.yml")

    def get_user_id(self):
        return self.raw_config["account"]["user_id"]

    def get_nick_name(self):
        return self.raw_config["account"]["nick_name"]

    def get_bot_admin(self):
        return self.raw_config["account"]["bot_admin"]

    def get_server_host(self):
        return self.raw_config["server"]["host"]

    def get_server_port(self):
        return self.raw_config["server"]["port"]

    def get_api_host(self):
        return self.raw_config["api"]["host"]

    def get_api_port(self):
        return self.raw_config["api"]["port"]
