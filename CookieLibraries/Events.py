# coding: utf-8

# Created by BigCookie233

import CookieLibraries.EventManager as EventManager
import CookieLibraries.PluginManager as PluginManager


def onEnable(func):
    return EventManager.event_listener(PluginManager.PluginEnableEvent)(func)


def onDisable(func):
    return EventManager.event_listener(PluginManager.PluginDisableEvent)(func)
