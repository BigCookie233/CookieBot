# coding: utf-8

# Created by BigCookie233

import importlib
import os

import CookieLibraries.EventManager as EventManager
import CookieLibraries.LoggerManager as LoggerManager


class PluginEvent(EventManager.Event):
    def __init__(self, instance):
        self.instance = instance

    def call(self):
        if self.instance.__name__ in EventManager.event_listeners:
            module = EventManager.event_listeners[self.instance.__name__]
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        LoggerManager.exception_handler(listener)(self)


class PluginEnableEvent(PluginEvent):
    def __init__(self, instance):
        super().__init__(instance)


class PluginDisableEvent(PluginEvent):
    def __init__(self, instance):
        super().__init__(instance)


class Plugin:
    def __init__(self, name, package="modules"):
        self.version = None
        self.instance = None
        self.name = name
        self.package = package

    def load(self):
        try:
            self.instance = importlib.import_module(name=self.name, package=self.package)
            self.version = self.instance.PLUGIN_VERSION
        except Exception as e:
            self.instance = None
            self.version = None
            LoggerManager.logger.error("An error occurred while loading {}: {}".format(self.name, e))

    def enable(self):
        PluginEnableEvent(self.instance).call()

    def disable(self):
        PluginDisableEvent(self.instance).call()


def load_module(name, package="modules"):
    module = Plugin(name, package)
    module.load()
    module.enable()
    return module


modules = {}


def load_modules(package):
    global modules
    for module_name in os.listdir(package):
        for suffix in [".py", ".pyc"]:
            if module_name.endswith(suffix):
                module_name = module_name.split(".")[0]
                module = load_module("." + module_name, package)
                if module.instance is not None:
                    modules[module_name] = module
