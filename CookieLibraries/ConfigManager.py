# coding: utf-8

# Created by BigCookie233

import yaml

from CookieLibraries import LoggerManager


class Config:
    def __init__(self, path, default_config=None):
        self.raw_config = None
        self.path = path
        self.default_config = default_config
        self.encoding = "utf-8"
        self.reload()

    @LoggerManager.exception_handler
    def reload(self):
        try:
            with open(self.path, "r", encoding=self.encoding) as file:
                self.raw_config = yaml.load(file.read(), yaml.FullLoader)
        except FileNotFoundError:
            if self.default_config is not None:
                if isinstance(self.default_config, str):
                    with open(self.path, "w", encoding=self.encoding) as file:
                        file.write(self.default_config)
                    self.raw_config = yaml.load(self.default_config, yaml.FullLoader)
                else:
                    raise TypeError("default config must be a string")
            else:
                raise FileNotFoundError("No such file and no default config set: {}".format(self.path))
