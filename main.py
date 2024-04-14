# coding:utf-8
from CookieLibraries.core import *
from CookieLibraries.extra import *
from CookieLibraries.protocol import *

VERSION = "2.2.0-dev"

# 主函数
if __name__ == '__main__':
    # Initialize
    CookieLibraries.init()
    # Start up
    logger = LoggerUtils.logger
    logger.info(f"Starting up CookieBot {VERSION}")
    # Load Config
    config = ConfigManager.GlobalConfig()
    # Load Plugins
    logger.info("Loading plugins...")
    PluginManager.load_plugins("plugins")
    logger.info(f"Loaded {len(PluginManager.plugins)} plugins")
    # Start Server
    Server.start()
