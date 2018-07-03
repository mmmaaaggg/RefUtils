# -*- coding: utf-8 -*-
"""
Created on 2017/7/12
@author: MG
"""
import logging
from datetime import timedelta, datetime
from threading import Thread
from pymongo import MongoClient
import time
from src.fh_tools.language_test.webscraping.s8tu.get_albums_2 import UserPage
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
logger = logging.getLogger()


class DownloadPicThread(Thread):
    def __init__(self, user_name, pange_num_start=10, step=10):
        super().__init__(name=user_name)
        self.user_name = user_name
        self.user_page = UserPage.builder(user_name, page_num_start=pange_num_start, step=step)
        self.beat()

    def beat(self):
        self._heart_beat_dt = datetime.now()

    def run(self):
        # 加载 用户首界面
        self.user_page.download(mode='images')

    @property
    def heart_beat_dt(self):
        if self.user_page is not None:
            heart_beat_dt_max = self.user_page.heart_beat_dt
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
        return self._heart_beat_dt

if __name__ == '__main__':

    user_name = 'yuehun'  # sisiwc  ly2160046 ssyxfhh
    pange_num_start = 10
    step = 40
    client = MongoClient('127.0.0.1', 27017)
    try:
        # download_pic_by_images(user_name)
        t = DownloadPicThread(user_name, pange_num_start=pange_num_start, step=step)
        # t.run()
        t.start()
        while 1:
            try:
                time.sleep(30)
                heart_beat_dt = t.heart_beat_dt
                if not t.is_alive():
                    logger.info('all finished')
                    break
                if datetime.now() - heart_beat_dt < timedelta(minutes=3):
                    logger.debug('beat %s', heart_beat_dt)
                    continue
                t.join(1)
                logger.warning('删除旧线程')
                t._delete()
            except:
                logger.exception('线程异常')

            logger.warning('重启线程')
            t = DownloadPicThread(user_name, pange_num_start=pange_num_start)
            t.start()
        # 相册下载测试
        # album_url_str = 'http://www.s8tu.com/album/xq'
        # download_pic_from_album(album_url_str)
    finally:
        client.close()