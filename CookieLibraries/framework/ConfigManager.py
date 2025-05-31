# coding: utf-8
# Created by BigCookie233
import traceback
import yaml
from os import path

from CookieLibraries.core.logger import traceback_exception
from CookieLibraries.core.injector import singleton
from CookieLibraries.framework import FileCacher


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path

    @traceback_exception
    def reload(self):
        with open(self.path, "r") as file:
            self.raw_config = yaml.load(file.read(), yaml.FullLoader)
        return self

    @traceback_exception
    def save_default(self, default_config: str):
        assert isinstance(default_config, str), "default config must be a string"
        if not path.exists(self.path):
            with open(self.path, "w") as file:
                file.write(default_config)
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
        super().__init__(path.join("configs",
                                   f"{path.splitext(
                                       path.split(
                                           traceback.extract_stack()[-2].filename
                                       )[-1]
                                   )[0]}.yml"))


@singleton
def global_config() -> GlobalConfig:
    return GlobalConfig()
