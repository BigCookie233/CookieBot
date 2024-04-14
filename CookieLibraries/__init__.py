# coding: utf-8

# Created by BigCookie233

import CookieLibraries.core
import CookieLibraries.extra
import CookieLibraries.protocol


def init():
    # Initialize Logger
    print("Initializing Logger")
    CookieLibraries.core.LoggerUtils.init("logs")
    # Initialize Controller
    CookieLibraries.core.LoggerUtils.logger.info("Initializing Controller")
    CookieLibraries.protocol.BotController.init()
    # Initialize Thread Pool
    CookieLibraries.core.LoggerUtils.logger.info("Initializing Thread Pool")
    CookieLibraries.core.ThreadPool.init()
