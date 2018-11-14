#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/11/14 13:24
@File    : spinner_asyncio.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import asyncio
import itertools
import sys


@asyncio.coroutine
def spin(msg):
    write, flush = sys.stdout.write, sys.stdout.flush
    for char in itertools.cycle('|/-\\'):
        status = char + ' ' + msg
        write(status)
        flush()
        write('\x08' * len(status))
        try:
            yield from asyncio.sleep(0.1)
        except asyncio.CancelledError:
            break
    write(' ' * len(status) + '\x08' * len(status))


@asyncio.coroutine
def slow_function():
    # 假装等待IO一段时间
    print('call slow_function')
    yield from asyncio.sleep(3)
    print('call slow_function finished')
    return 42


@asyncio.coroutine
def supervisor():
    spinner = asyncio.async(spin('thinking'))
    print('spinner object:', spinner)
    print('yield from ', slow_function())
    result = yield from slow_function()
    print('spinner.cancel()')
    spinner.cancel()
    return result


def main():
    loop = asyncio.get_event_loop()
    result = loop.run_until_complete(supervisor())
    loop.close()
    print('Answer:', result)


if __name__ == "__main__":
    main()
