# coding: utf-8
# Created by BigCookie233
import os
import warnings

import CookieLibraries.framework.Cacher as Cacher


@Cacher.cache()
def read_file(path):
    with open(path, "r") as file:
        return file.read()


def write_file(path, data):
    warnings.warn("the write_non_existent_file() is deprecated", DeprecationWarning)

    # @ThreadPool.async_task
    def write_file_task():
        with open(path, "w") as file:
            file.write(data)

    read_file.cache(path)(data)
    write_file_task()


def write_non_existent_file(path, data):
    warnings.warn("the write_non_existent_file() is deprecated", DeprecationWarning)

    def write_file_task():
        if not os.path.exists(path):
            write_file(path, data)

    read_file.cache((path,), {}, data)
    write_file_task(path, data)
