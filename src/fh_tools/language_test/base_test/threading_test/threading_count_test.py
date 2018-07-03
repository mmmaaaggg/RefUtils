# -*- coding: utf-8 -*-
"""
Created on 2017/6/13
@author: MG
"""

import threading
import time


class Counter:

    request_id = 0
    mutex = threading.Lock()

    def getter(self):
        self.mutex.acquire()
        self.request_id += 1
        time.sleep(1)
        self.mutex.release()
        return self.request_id


class Consumer(threading.Thread):

    def __init__(self, counter):
        super().__init__()
        self.counter = counter

    def run(self):
        self.consum()

    def consum(self):
        print(self.counter.getter())

if __name__ == '__main__':
    counter = Counter()
    for n in range(5):
        consumer = Consumer(counter)
        consumer.start()
    time.sleep(10)
