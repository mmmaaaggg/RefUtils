# -*- coding: utf-8 -*-
"""
Created on 2017/6/9
@author: MG
threading.Event机制类似于一个线程向其它多个线程发号施令的模式，其它线程都会持有一个threading.Event的对象，这些线程都会等待这个事件的“发生”，如果此事件一直不发生，那么这些线程将会阻塞，直至事件的“发生”。
对此，我们可以考虑一种应用场景（仅仅作为说明），例如，我们有多个线程从Redis队列中读取数据来处理，这些线程都要尝试去连接Redis的服务，一般情况下，如果Redis连接不成功，在各个线程的代码中，都会去尝试重新连接。如果我们想要在启动时确保Redis服务正常，才让那些工作线程去连接Redis服务器，那么我们就可以采用threading.Event机制来协调各个工作线程的连接操作：主线程中会去尝试连接Redis服务，如果正常的话，触发事件，各工作线程会尝试连接Redis服务。
为此，我们可以写下如下的程序：
"""
import threading
import time
import logging

logging.basicConfig(level=logging.DEBUG, format='(%(threadName)-10s) %(message)s', )


def worker(event):
    logging.debug('Waiting for redis ready...')
    event.wait()
    logging.debug('redis ready, and connect to redis server and do some work [%s]', time.ctime())
    time.sleep(1)


readis_ready = threading.Event()
t1 = threading.Thread(target=worker, args=(readis_ready,), name='t1')
t1.start()

t2 = threading.Thread(target=worker, args=(readis_ready,), name='t2')
t2.start()

logging.debug('first of all, check redis server, make sure it is OK, and then trigger the redis ready event')
time.sleep(3)  # simulate the check progress
readis_ready.set()
