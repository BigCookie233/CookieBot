# coding: utf-8
# Created by BigCookie233
import atexit
import logging
from concurrent.futures import ThreadPoolExecutor
from functools import wraps

from .config import Config
from .injector import inject, singleton


class ThreadPoolConfig(Config):
    def __init__(self):
        self.max_workers = 5


@singleton
def threadpool_config() -> ThreadPoolConfig:
    return ThreadPoolConfig()


@singleton
def threadpool(logger: logging.Logger, config: ThreadPoolConfig) -> ThreadPoolExecutor:
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
