# coding:utf-8

from logging import Logger

from CookieLibraries.core import *
from CookieLibraries.protocol import *

VERSION = "2.3.0-dev"

# 主函数
if __name__ == '__main__':
    # Initialize
    Bootstrap.main()
    # Start up
    logger = DependencyInjector.get_instance(Logger)
    logger.info(f"Starting up CookieBot {VERSION}")
    # Load Config
    config = DependencyInjector.get_instance(ConfigManager.GlobalConfig)
    # Load Plugins
    logger.info("Loading plugins...")
    PluginManager.load_plugins("plugins")
    logger.info(f"Loaded {len(PluginManager.plugins)} plugins")
    # Start Server
    Server.start()
