# coding: utf-8

# Created by BigCookie233

import CookieLibraries.ConfigManager as ConfigManager

global_config = None


class GlobalConfig(ConfigManager.Config):
    def __init__(self):
        super().__init__("config.yml")
        self.reload()
        self.server_host = self.raw_config["server"]["host"]
        self.server_port = self.raw_config["server"]["port"]
        self.api_host = self.raw_config["api"]["host"]
        self.api_port = self.raw_config["api"]["port"]
        self.max_workers = self.raw_config["thread_pool"]["max_workers"]
