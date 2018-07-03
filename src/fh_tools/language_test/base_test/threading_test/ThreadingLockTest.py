# -*- coding:utf-8 -*-
'''
Created on 2017年2月14日

@author: Family
'''
from threading import Thread, Lock
import time

counterlist = [0]
mutex = Lock()


class Counter(Thread):
    
    def __init__(self):
        Thread.__init__(self)
    
    def run(self):
        global counterlist, mutex
        time.sleep(1);
        if mutex.acquire():
            counterlist.append(counterlist[-1]+1)
            print("I am %s, set counter:%s" % (self.name, len(counterlist)))
            mutex.release()


class Counter2(Thread):
    def __init__(self, with_lock):
        Thread.__init__(self)
        self.with_lock = with_lock

    def run(self):
        global counterlist, mutex
        time.sleep(1)
        if self.with_lock:
            with mutex:
                counterlist.append(counterlist[-1] + 1)
                print("I am %s" % self.name)
                print(">set counter:%s" % len(counterlist))
        else:
            counterlist.append(counterlist[-1] + 1)
            print("I am %s" % self.name)
            print(">set counter:%s" % len(counterlist))

if __name__ == '__main__':
    for i in range(100):
        mythread = Counter2(True)
        mythread.start()
    print('counterlist:', counterlist)
    time.sleep(2)
    print('after 2 seconds\ncounterlist:', counterlist)