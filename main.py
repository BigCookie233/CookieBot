# coding:utf-8

from logging import Logger

from CookieLibraries.core import *
from CookieLibraries.framework import *
from CookieLibraries.protocol import *

VERSION = "2.3.0-dev"


@inject
def main(logger: Logger, config: GlobalConfig):
    # Initialize
    bootstrap.main()
    # Start up
    logger.info(f"Starting up CookieBot {VERSION}")
    # Load Plugins
    logger.info("Loading plugins...")
    PluginManager.load_plugins("plugins")
    logger.info(f"Loaded {len(PluginManager.plugins)} plugins")
    # Start Server
    Server.start()


# 主函数
if __name__ == '__main__':
    main()
