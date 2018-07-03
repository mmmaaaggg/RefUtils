# -*- coding: utf-8 -*-
"""
Created on 2017/7/15
@author: MG
"""

from queue import Queue, Empty
from threading import Thread
import time
import logging

logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
logger = logging.getLogger()
product_queue = Queue()


class Productor(Thread):

    def run(self):
        for n in range(20):
            prodcut_info = {'product sn': n}
            product_queue.put(prodcut_info)
            logger.info('>>>   %s', prodcut_info)
            time.sleep(0.5)
        logging.info('finished all products')


class Consumer(Thread):

    def run(self):
        while 1:
            try:
                logging.info('   <<<%s', product_queue.get(True, 0.1))
                product_queue.task_done()
            except Empty:
                logging.warning('queue empty')
                time.sleep(3)

if __name__ == "__main__":
    consumer = Consumer()
    productor = Productor()
    consumer.setDaemon(True)
    productor.setDaemon(True)
    consumer.start()
    productor.start()
    productor.join()
    logging.info('wait queue finished')
    product_queue.join()
    logging.info('all finished')