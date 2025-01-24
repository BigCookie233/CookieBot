# coding: utf-8
# Created by BigCookie233
import importlib
import os
from logging import Logger

from .DependencyInjector import inject
from .EventManager import Event


class PluginEvent(Event):
    def __init__(self, instance):
        super().__init__()
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


class PreLoadPluginsEvent(Event):
    pass


class PostLoadPluginsEvent(Event):
    pass


class Plugin:
    def __init__(self, module_name, package="plugins"):
        self.name = None
        self.version = None
        self.instance = None
        self.module_name = module_name
        self.package = package

    @inject
    def load(self, logger: Logger = inject):
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

    @inject
    def enable(self, logger: Logger = inject):
        logger.info(f"Enabling {self.name} v{self.version}")
        PluginEnableEvent(self.instance).call()

    @inject
    def disable(self, logger: Logger = inject):
        logger.info(f"Disabling {self.name} v{self.version}")
        PluginDisableEvent(self.instance).call()


def load_plugin(name, package="plugins"):
    module = Plugin(name, package)
    module.load()
    if module.instance is not None:
        module.enable()
        plugins[name] = module


plugins = {}


@inject
def load_plugins(package, logger: Logger = inject):
    global plugins
    PreLoadPluginsEvent().call()
    try:
        for plugin_name in os.listdir(package):
            for suffix in [".py", ".pyc"]:
                if plugin_name.endswith(suffix):
                    load_plugin("." + plugin_name.split(".")[0], package)
    except Exception as e:
        logger.error("An error occurred while loading plugins: {}".format(e))
        raise
    PostLoadPluginsEvent().call()
