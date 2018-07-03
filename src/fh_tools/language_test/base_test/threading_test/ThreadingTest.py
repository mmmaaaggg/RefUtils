#!/usr/bin/env python
import threading
from time import sleep

def thread1(tot_count):
    for i in range(tot_count):
        print('this is thread 1...%d' % i)
        sleep(2)

def thread2():
    for i in range(3):
        print('this is thread 2...%d' % i)
        sleep(3)

t1=threading.Thread(target=thread1, args=(3,))
t2=threading.Thread(target=thread2)
# t1.setDaemon(True)
# t2.setDaemon(True)
t1.start()
t2.start()
sleep(5)
print('all over')