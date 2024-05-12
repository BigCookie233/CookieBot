# coding: utf-8

# Created by BigCookie233

import os
import traceback

import yaml

from CookieLibraries.core import FileCacher
from CookieLibraries.core import LoggerUtils
from CookieLibraries.core.DependencyInjector import bean


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path

    @LoggerUtils.log_exception()
    def reload(self):
        self.raw_config = yaml.load(FileCacher.read_file(self.path), yaml.FullLoader)
        return self

    @LoggerUtils.log_exception()
    def save_default(self, default_config: str):
        if isinstance(default_config, str):
            FileCacher.write_non_existent_file(self.path, default_config)
        else:
            raise TypeError("default config must be a string")
        return self


class GlobalConfig(Config):
    def __init__(self):
        super().__init__("config.yml")
        self.reload()
        self.server_host = self.raw_config["server"]["host"]
        self.server_port = self.raw_config["server"]["port"]
        self.api_host = self.raw_config["api"]["host"]
        self.api_port = self.raw_config["api"]["port"]
        self.max_workers = self.raw_config["thread_pool"]["max_workers"]


class PluginConfig(Config):
    def __init__(self):
        super().__init__(os.path.join("configs", traceback.extract_stack()[-2].filename.rsplit(".", 1)[0] + ".yml"))


@bean
def global_config() -> GlobalConfig:
    return GlobalConfig()
