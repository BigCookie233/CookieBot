# coding: utf-8

# Created by BigCookie233

import os

import CookieLibraries.core.Cacher as Cacher
import CookieLibraries.core.ThreadPool as ThreadPool


@Cacher.cache()
def read_file(path):
    with open(path, "r") as file:
        return file.read()


def write_file(path, data):
    @ThreadPool.async_task
    def write_file_task():
        with open(path, "w") as file:
            file.write(data)

    read_file.cache(path)(data)
    write_file_task()


def write_non_existent_file(path, data):
    @ThreadPool.async_task
    def write_file_task():
        if not os.path.exists(path):
            write_file(path, data)

    read_file.cache((path,), {}, data)
    write_file_task(path, data)
