# coding: utf-8

# Created by BigCookie233

import CookieLibraries.BotController
import CookieLibraries.ConfigManager
import CookieLibraries.Configs
import CookieLibraries.EventManager
import CookieLibraries.Events
import CookieLibraries.ExceptionHandler
import CookieLibraries.LoggerManager
import CookieLibraries.MessageManager
import CookieLibraries.PluginManager
import CookieLibraries.ThreadPool


def init():
    # Initialize Logger
    print("Initializing Logger")
    LoggerManager.init("logs")
    # Initialize Controller
    LoggerManager.logger.info("Initializing Controller")
    BotController.init()
    # Initialize Thread Pool
    LoggerManager.logger.info("Initializing Thread Pool")
    ThreadPool.init()
