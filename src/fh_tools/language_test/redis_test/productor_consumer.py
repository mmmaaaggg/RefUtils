# -*- coding: utf-8 -*-
"""
Created on 2017/7/17
@author: MG
"""
from threading import Thread
from redis import StrictRedis, ConnectionPool
import time
from datetime import  datetime
import logging
from src.fh_tools.fh_utils import bytes_2_str
import json
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
logger = logging.getLogger()
conn_pool = ConnectionPool(host='192.168.159.131', port=6379, db=1)


class Productor(Thread):
    def run(self):
        r = StrictRedis(connection_pool=conn_pool)

        for n in range(10):
            if n == 9:
                r.publish('pubsub_msg', 'over')
            else:
                r.publish('pubsub_msg', {'pub_time': datetime.now()})
            time.sleep(1)


class Consumer(Thread):
    def run(self):
        r = StrictRedis(connection_pool=conn_pool)
        pub_sub = r.pubsub()
        pub_sub.subscribe('pubsub_msg')
        for item in pub_sub.listen():
            logger.debug(item)
            if item['type'] == 'message':
                msg_data = item['data']
                if msg_data == b'over':
                    break
                # else:
                #     msg_str = bytes_2_str(msg_data)
                #     logger.debug('msg_str:%s', msg_str)
                #     msg_dic = json.loads(msg_str)
                #     logger.debug('time delta:%s', msg_dic['pub_time'] - datetime.now())

if __name__ == "__main__":
    productor = Productor()
    productor.setDaemon(True)
    consumer = Consumer()
    consumer.start()
    productor.start()
    consumer.join()


