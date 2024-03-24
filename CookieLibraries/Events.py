# coding: utf-8

# Created by BigCookie233

import CookieLibraries.EventManager as EventManager
import CookieLibraries.PluginManager as PluginManager


def on_enable(func):
    @EventManager.event_listener(PluginManager.PluginEnableEvent)
    def wrapper(event):
        func()

    return wrapper


def on_disable(func):
    @EventManager.event_listener(PluginManager.PluginDisableEvent)
    def wrapper(event):
        func()

    return wrapper
