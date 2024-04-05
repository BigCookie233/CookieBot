# coding: utf-8

# Created by BigCookie233

import CookieLibraries.extra
import CookieLibraries.core


def init():
    # Initialize Logger
    print("Initializing Logger")
    CookieLibraries.core.LoggerManager.init("logs")
    # Initialize Controller
    CookieLibraries.core.LoggerManager.logger.info("Initializing Controller")
    CookieLibraries.core.BotController.init()
    # Initialize Thread Pool
    CookieLibraries.core.LoggerManager.logger.info("Initializing Thread Pool")
    CookieLibraries.core.ThreadPool.init()
