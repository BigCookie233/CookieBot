# coding: utf-8
# Created by BigCookie233
from logging import Logger

import CookieLibraries.core
import CookieLibraries.extra
import CookieLibraries.protocol


@CookieLibraries.core.DependencyInjector.autowired
def init(logger: Logger):
    CookieLibraries.core.DependencyInjector.initialize_all_beans()
    # Initialize Controller
    logger.info("Initializing Controller")
    CookieLibraries.protocol.BotController.init()
