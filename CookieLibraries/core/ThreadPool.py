# coding: utf-8

# Created by BigCookie233

import importlib
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

import atexit

from .DependencyInjector import bean, get_instance, autowired


@bean
def threadpool(logger: logging.Logger) -> ThreadPoolExecutor:
    logger.info("Initializing Thread Pool")
    config = importlib.import_module(name="CookieLibraries.core.ConfigManager").GlobalConfig()
    return ThreadPoolExecutor(max_workers=config.max_workers)


def async_task(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        get_instance(ThreadPoolExecutor).submit(func, *args, **kwargs)

    return wrapper


@atexit.register
@autowired
def shutdown(thread_pool: ThreadPoolExecutor, logger: logging.Logger):
    logger.info("Closing Thread Pool")
    thread_pool.shutdown()
