# coding: utf-8
# Created by BigCookie233
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import atexit

from .ConfigManager import GlobalConfig
from .DependencyInjector import provider, inject


@provider
def threadpool(logger: logging.Logger, config: GlobalConfig) -> ThreadPoolExecutor:
    logger.info("Initializing Thread Pool")
    return ThreadPoolExecutor(max_workers=config.max_workers)


@inject
def async_task(func, thread_pool: ThreadPoolExecutor = inject):
    @wraps(func)
    def wrapper(*args, **kwargs):
        thread_pool.submit(func, *args, **kwargs)

    return wrapper


@atexit.register
@inject
def shutdown(thread_pool: ThreadPoolExecutor, logger: logging.Logger):
    logger.info("Closing Thread Pool")
    thread_pool.shutdown()
