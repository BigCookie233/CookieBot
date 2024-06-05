# coding: utf-8

# Created by BigCookie233

import importlib
import os
from logging import Logger

from .EventManager import Event
from .DependencyInjector import autowired


class PluginEvent(Event):
    def __init__(self, instance):
        self.instance = instance

    @property
    def listeners(self):
        for listener in super().listeners:
            if listener.callback.__module__ == self.instance.__name__:
                yield listener


class PluginEnableEvent(PluginEvent):
    def __init__(self, instance):
        super().__init__(instance)


class PluginDisableEvent(PluginEvent):
    def __init__(self, instance):
        super().__init__(instance)


class Plugin:
    def __init__(self, module_name, package="plugins"):
        self.name = None
        self.version = None
        self.instance = None
        self.module_name = module_name
        self.package = package

    @autowired
    def load(self, logger: Logger = autowired):
        try:
            self.instance = importlib.import_module(name=self.module_name, package=self.package)
            self.name = self.instance.PLUGIN_NAME
            self.version = self.instance.PLUGIN_VERSION
        except Exception as e:
            self.unload()
            logger.error("An error occurred while loading {}: {}".format(self.module_name, e))

    def unload(self):
        self.instance = None
        self.name = None
        self.version = None

    @autowired
    def enable(self, logger: Logger = autowired):
        logger.info(f"Enabling {self.name} v{self.version}")
        PluginEnableEvent(self.instance).call()

    @autowired
    def disable(self, logger: Logger = autowired):
        logger.info(f"Disabling {self.name} v{self.version}")
        PluginDisableEvent(self.instance).call()


def load_plugin(name, package="plugins"):
    module = Plugin(name, package)
    module.load()
    if module.instance is not None:
        module.enable()
        plugins[name] = module


plugins = {}

@autowired
def load_plugins(package, logger: Logger = autowired):
    global plugins
    try:
        for plugin_name in os.listdir(package):
            for suffix in [".py", ".pyc"]:
                if plugin_name.endswith(suffix):
                    load_plugin("." + plugin_name.split(".")[0], package)
    except Exception as e:
        logger.error("An error occurred while loading plugins: {}".format(e))
        raise
