# coding: utf-8

# Created by BigCookie233

import CookieLibraries.EventManager as EventManager
import CookieLibraries.ModuleManager as ModuleManager


def onEnable():
    return EventManager.event_listener(ModuleManager.ModuleEnableEvent)


def onDisable():
    return EventManager.event_listener(ModuleManager.ModuleDisableEvent)
