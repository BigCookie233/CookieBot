# coding: utf-8
# Created by BigCookie233
import traceback
from os import path

import yaml

from . import FileCacher
from .DependencyInjector import bean
from .LoggerUtils import traceback_exception


class Config:
    def __init__(self, path):
        self.raw_config = None
        self.path = path

    @traceback_exception
    def reload(self):
        self.raw_config = yaml.load(FileCacher.read_file(self.path), yaml.FullLoader)
        return self

    @traceback_exception
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
        super().__init__(path.join("configs",
                                   f"{path.splitext(
                                       path.split(
                                           traceback.extract_stack()[-2].filename
                                       )[-1]
                                   )[0]}.yml"))


@bean
def global_config() -> GlobalConfig:
    return GlobalConfig()
