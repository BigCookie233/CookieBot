# coding: utf-8

# Created by BigCookie233

import importlib

import CookieLibraries.EventManager as EventManager
import CookieLibraries.LoggerManager as LoggerManager


class ModuleEvent(EventManager.Event):
    def __init__(self, instance):
        self.instance = instance

    def call(self):
        if self.instance.__name__ in EventManager.event_listeners:
            module = EventManager.event_listeners[self.instance.__name__]
            if self.__class__ in module:
                for priority in sorted(module[self.__class__].keys(), key=lambda x: x.value):
                    for listener in module[self.__class__][priority]:
                        try:
                            listener(self)
                        except Exception as e:
                            LoggerManager.logger.error("Caught {} when call listener: {}".format(e, listener))


class ModuleEnableEvent(ModuleEvent):
    def __init__(self, instance):
        super().__init__(instance)


class ModuleDisableEvent(ModuleEvent):
    def __init__(self, instance):
        super().__init__(instance)


class Module:
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
            LoggerManager.logger.error("Caught {} when load module: {} in {}".format(e, self.name, self.package))

    def enable(self):
        ModuleEnableEvent(self.instance).call()

    def disable(self):
        ModuleDisableEvent(self.instance).call()


def load_module(name, package="modules"):
    module = Module(name, package)
    module.load()
    module.enable()
    return module
