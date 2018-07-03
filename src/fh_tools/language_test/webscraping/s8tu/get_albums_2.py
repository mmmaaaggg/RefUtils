# -*- coding: utf-8 -*-
"""
Created on 2017/7/7
@author: MG
"""
from pymongo.database import Database
from pymongo.collection import Collection
from datetime import datetime, timedelta
from threading import Thread, Lock
from urllib.request import urlopen
import logging
from bs4 import BeautifulSoup as bs
from pymongo import MongoClient
from requests import HTTPError
from http.client import IncompleteRead
import numpy as np
import re
import time
from os import path, makedirs
import urllib
logging.basicConfig(level=logging.DEBUG,
                    format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
logger = logging.getLogger()


class ConfigBase:
    ROOT_FOLDER_PATH = r'd:\Downloads\other'
    # 支持 jpg、png格式，日后有新格式再添加
    RE_MD_PATTERN = re.compile(r"(.+).md.(jpg|png)")
    RE_IMG_TAG_PATTERN = re.compile(r".+\.md\.(jpg|png)")

    # mongo db info
    MONGO_INFO_DIC = {'MONGO_DB_URL': '10.0.3.66',
                      'MONGO_DB_PORT': 27017,
                      'MONGO_DB_NAME': 'test',
                      }
    __MONGO_CLIENT = None
    IMAGE_LIST_COLLECTION_NAME = 's8tu:image_list'
    ALBUM_COLLECTION_NAME = 's8tu:album'
    IMAGE_COLLECTION_NAME = 's8tu:image'

    def get_db_client(self) -> MongoClient:
        """
        获取mongodb client
        :return: 
        """
        if self.__MONGO_CLIENT is None:
            self.__MONGO_CLIENT = MongoClient('mongodb://%s:%s/' % (self.MONGO_INFO_DIC['MONGO_DB_URL'],
                                                                    self.MONGO_INFO_DIC['MONGO_DB_PORT']))
        return self.__MONGO_CLIENT

    def get_db_database(self, db_name=None) -> Database:
        """
        获取 mongodb database
        :param db_name: 
        :return: 
        """
        client = self.get_db_client()
        if db_name is None:
            db_name = self.MONGO_INFO_DIC['MONGO_DB_NAME']
        return client[db_name]

    def get_db_collection(self, collection_name, db_name=None) -> Collection:
        """
        获取 mongodb collection
        :param collection_name: 
        :param db_name: 
        :return: 
        """
        database = self.get_db_database(db_name)
        return database[collection_name]

    def release(self):
        """
        释放资源
        :return: 
        """
        if self.__MONGO_CLIENT is not None:
            self.__MONGO_CLIENT.close()
Config = ConfigBase()

class Page:
    def __init__(self, url_str):
        self.url_str = url_str
        self._bsobj = None
        self._html_str = None
        self.beat()
        self.lock = Lock()

    def beat(self):
        self._heart_beat_dt = datetime.now()
        return self._heart_beat_dt

    @property
    def heart_beat_dt(self):
        return self._heart_beat_dt

    @property
    def bsobj(self):
        if self._bsobj is None:
            self._bsobj = bs(self.load(), "lxml")
        return self._bsobj

    def load(self):
        if self.lock.acquire():
            try:
                if self._html_str is None:
                    try_count = 0
                    max_try_count = 3
                    for try_count in range(max_try_count):
                        try:
                            logger.info('加载：%s', self.url_str)
                            with urlopen(self.url_str) as rsp:
                                self._html_str = rsp.read().decode('utf-8')
                                self.beat()
                            break
                        except IncompleteRead:
                            logger.exception('加载：%s 失败', self.url_str)
                        except HTTPError as exp:
                            if exp.code == 500:
                                logger.info('加载：%s 失败，找不到页面', self.url_str)
                                self.beat()
                                break
                            else:
                                logger.exception('加载：%s', self.url_str)
            finally:
                self.lock.release()
                self.beat()
        return self._html_str

    def download(self):
        self.beat()


class UserPage(Page):
    def __init__(self, url_str, user_name, page_num_start, step=4):
        super().__init__(url_str)
        self.user_name = user_name
        self.page_num_start = page_num_start
        self.step = step
        self.album_list_page = None
        self.image_list_page = None

    @staticmethod
    def builder(user_name, page_num_start=4, step=4):
        url_str = 'http://www.s8tu.com/%s' % user_name
        return UserPage(url_str, user_name, page_num_start, step=step)

    @property
    def album_count(self):
        bsobj = self.bsobj
        obj = bsobj.find("b", {"data-text": "album-count"})
        return int(obj.contents[0])

    @property
    def image_count(self):
        bsobj = self.bsobj
        obj = bsobj.find("b", {"data-text": "image-count"})
        return int(obj.contents[0])

    def download(self, mode='albums'):
        """ mode: albums images"""
        if mode == 'albums':
            self.download_albums()
        else:
            self.download_images()

    def download_albums(self):
        # 计算 相册列表页 页数
        album_count = self.album_count
        if album_count <= 32:
            page_list = [1]
        elif album_count <= 32 * self.step:
            page_list = [int(np.ceil(float(album_count) / 32))]
        else:
            page_list = list(set(np.arange(self.page_num_start, int(np.ceil(float(album_count) / 32)), self.step)) |
                             {int(np.ceil(float(album_count) / 32))})
            page_list.sort()
        for page_num in page_list:
            self.album_list_page = AlbumListPage.builder(self.user_name, page_num)
            self.album_list_page.download()
        self.beat()

    def download_images(self):
        # 计算 图片列表页 页数
        image_count = self.image_count
        if image_count <= 32:
            page_list = [1]
        elif image_count <= 32 * self.step:
            page_list = [int(np.ceil(float(image_count) / 32))]
        else:
            page_list = list(set(np.arange(self.page_num_start, int(np.ceil(float(image_count) / 32)), self.step)) |
                             {int(np.ceil(float(image_count) / 32))})
            page_list.sort()
        for page_num in page_list:
            self.image_list_page = ImageListPage.builder(self.user_name, page_num)
            self.image_list_page.download()
        self.beat()

    @property
    def heart_beat_dt(self):
        if self.album_list_page is not None:
            logger.debug('heart_beat_dt album_list_page')
            heart_beat_dt_max = self.album_list_page.heart_beat_dt
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
        elif self.image_list_page is not None:
            logger.debug('heart_beat_dt image_list_page')
            heart_beat_dt_max = self.image_list_page.heart_beat_dt
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
        return self._heart_beat_dt


class ImageListPage(Page):
    def __init__(self, url_str, user_name, page_num):
        super().__init__(url_str)
        self.user_name = user_name
        self.page_num = page_num
        self._image_count = None
        self.image_page_list = []

    @property
    def image_count(self):
        if self._image_count is None:
            bsobj = self.bsobj
            obj = bsobj.find("b", {"data-text": "image-count"})
            self._image_count = int(obj.contents[0])
        return self._image_count

    @property
    def img_info_dic_list(self):
        bsobj = self.bsobj
        link_list = bsobj.findAll("a", {"class": "image-container"})
        pair_list = []
        for link in link_list:
            try:
                image_md_url = link.find("img", src=Config.RE_IMG_TAG_PATTERN)['src']
            except:
                image_md_url = link.find("img")['src']
                logger.warning('%s 无法匹配%s 直接下载', image_md_url, Config.RE_IMG_TAG_PATTERN)
            finally:
                img_page_url = link['href']
                pair_list.append({'img_page_url': img_page_url,
                                  'image_md_url': image_md_url})
        return pair_list

    @staticmethod
    def builder(user_name, page_num=4):
        if page_num is None:
            url_str = "http://www.s8tu.com/%s/?list=images&sort=date_desc&page=1" % user_name  # date_desc date_asc
        else:
            url_str = "http://www.s8tu.com/%s/?list=images&sort=date_desc&page=%d" % (user_name, page_num)
        return ImageListPage(url_str, user_name, page_num)

    @property
    def has_been_download(self):
        """检查是否当前List已经被下载"""
        collection = Config.get_db_collection(Config.IMAGE_LIST_COLLECTION_NAME)
        key = 'url'
        url_str = self.url_str
        content = collection.find_one({key: url_str})
        is_done = content is not None
        if is_done:
            logger.info('图片列表：%s [%d]已经被下载完成', url_str, self.image_count)
        return is_done

    def download(self):
        if not self.has_been_download:
            img_info_dic_list = self.img_info_dic_list
            collection = Config.get_db_collection(Config.IMAGE_LIST_COLLECTION_NAME)
            success_count = 0
            for n, img_info_dic in enumerate(img_info_dic_list):
                image_md_url = img_info_dic['image_md_url']
                image_url = Config.RE_MD_PATTERN.sub(r'\1.\2', image_md_url)
                index = image_url.rindex('/')
                file_name = image_url[(index + 1):]
                image_obj = ImagePage(image_url, self.user_name,
                                      album_name=None, file_name=file_name, img_info_dic=img_info_dic)
                self.image_page_list.append(image_obj)
                try:
                    image_obj.download()
                    success_count += 1
                except:
                    logger.exception('图片%d/%d) %s 下载失败', n, self.image_count, image_url)
            dic = {'url': self.url_str,
                   'image_count': success_count,
                   'datetime': self.beat(),
                   'tot_image_count': self.image_count,
                   }
            collection = Config.get_db_collection(Config.IMAGE_LIST_COLLECTION_NAME)
            collection.insert_one(dic)
        self.beat()

    @property
    def heart_beat_dt(self):
        image_page_list = self.image_page_list
        if len(image_page_list) == 0:
            return self._heart_beat_dt
        else:
            heart_beat_dt_max = max([image_page.heart_beat_dt for image_page in image_page_list])
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
            return self._heart_beat_dt


class AlbumListPage(Page):
    def __init__(self, url_str, user_name, page_num):
        super().__init__(url_str)
        self.user_name = user_name
        self.page_num = page_num
        self._album_list = None

    @property
    def album_list(self):
        bsobj = self.bsobj
        if self._album_list is None or len(self._album_list) == 0:
            self._album_list = []
            container_list = bsobj.findAll("div", {"class": "list-item-desc"})
            for container in container_list:
                link = container.find("a", {"data-text": "album-name"})
                album_url = link['href']
                album_name = link.contents[0]
                album_image_count = int(container.findAll("div")[1].findAll("span")[0].contents[0])
                self._album_list.append(AlbumPage(album_url, self.user_name, album_name, album_image_count))
        return self._album_list

    @staticmethod
    def builder(user_name, page_num=4):
        if page_num is None:
            url_str = "http://www.s8tu.com/%s/albums" % user_name
        else:
            url_str = "http://www.s8tu.com/%s/albums/?sort=date_asc&page=%d" % (user_name, page_num)
        return AlbumListPage(url_str, user_name, page_num)

    def download(self):
        album_list = self.album_list
        # 加载相册列表页
        for album in album_list:
            album.download()
        self.beat()

    @property
    def heart_beat_dt(self):
        album_list = self.album_list
        if album_list is None:
            return self._heart_beat_dt
        else:
            heart_beat_dt_max = max([album.heart_beat_dt for album in album_list])
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
            return self._heart_beat_dt


class AlbumPage(Page):
    def __init__(self, base_url_str, user_name, album_name, image_count):
        page_num = int(np.ceil(float(image_count) / 32))
        url_str = base_url_str + '/?sort=date_asc&page=%d' % page_num
        super().__init__(url_str)
        self.base_url_str = base_url_str
        self.user_name = user_name
        self.album_name = album_name
        self.image_count = image_count
        self.page_num = page_num
        self.image_page_list = []

    @property
    def image_md_list(self):
        bsobj = self.bsobj
        img_list = bsobj.findAll("img", src=Config.RE_IMG_TAG_PATTERN)
        img_url_list = [link['src'] for link in img_list]
        return img_url_list

    @property
    def img_info_dic_list(self):
        bsobj = self.bsobj
        div_obj_list = bsobj.findAll("div", {'data-type': 'image'})
        pair_list = []
        for div in div_obj_list:
            image_md_url = div.find("img", src=Config.RE_IMG_TAG_PATTERN)['src']
            img_page_url = div.find("a", {"class": "image-container"})['href']
            pair_list.append({'img_page_url': img_page_url,
                              'image_md_url': image_md_url})
        return pair_list

    @property
    def has_been_download(self):
        """检查是否当前相册以及被下载"""
        collection = Config.get_db_collection(Config.ALBUM_COLLECTION_NAME)
        key = 'url'
        url_str = self.url_str
        content = collection.find_one({key: url_str})
        is_done = content is not None
        if is_done:
            logger.info('相册 %s：%s [%d]已经被下载完成', self.album_name, url_str, self.image_count)
        return is_done

    def download(self):
        if not self.has_been_download:
            img_info_dic_list = self.img_info_dic_list
            collection = Config.get_db_collection(Config.ALBUM_COLLECTION_NAME)
            success_count = 0
            for n, img_info_dic in enumerate(img_info_dic_list):
                image_md_url = img_info_dic['image_md_url']
                image_url = Config.RE_MD_PATTERN.sub(r'\1.jpg', image_md_url)
                index = image_url.rindex('/')
                file_name = image_url[(index + 1):]
                image_obj = ImagePage(image_url, self.user_name, self.album_name, file_name, img_info_dic)
                self.image_page_list.append(image_obj)
                try:
                    image_obj.download()
                    success_count += 1
                except:
                    logger.exception('相册:【%s】 %d) %s 下载失败', self.album_name, n, image_url)
            dic = {'url': self.url_str,
                   'image_count': success_count,
                   'datetime': self.beat(),
                   'tot_image_count': self.image_count,
                   }
            collection = Config.get_db_collection(Config.ALBUM_COLLECTION_NAME)
            collection.insert_one(dic)
        self.beat()

    @property
    def heart_beat_dt(self):
        image_page_list = self.image_page_list
        if len(image_page_list) > 0:
            heart_beat_dt_max = max([image_page.heart_beat_dt for image_page in image_page_list])
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
        return self._heart_beat_dt


class ImagePage(Page):
    def __init__(self, url, user_name, album_name, file_name, img_info_dic):
        super().__init__(url)
        self.user_name = user_name
        self.album_name = album_name
        self.file_name = file_name
        img_info_dic['user_name'] = user_name
        img_info_dic['album_name'] = album_name
        img_info_dic['file_name'] = file_name
        self.img_info_dic = img_info_dic

    @property
    def has_been_download(self):
        """检查是否当前相册以及被下载"""
        collection = Config.get_db_collection(Config.IMAGE_COLLECTION_NAME)
        key = 'url'
        url_str = self.url_str
        content = collection.find_one({key: url_str})
        is_done = content is not None
        if is_done:
            if self.album_name is None:
                logger.info('图片：%s 已经被下载完成', url_str)
            else:
                logger.info('相册：【%s】 图片：%s 已经被下载完成', self.album_name, url_str)
        return is_done

    def download(self):
        if not self.has_been_download:

            file_path = self.file_path
            logger.debug('图片保存到：%s 网址：%s', file_path, self.url_str)
            with urlopen(self.url_str) as rsp:
                content = rsp.read()
            with open(file_path, mode='wb') as output:
                output.write(content)
            self.img_info_dic['url'] = self.url_str
            self.img_info_dic['file_path'] = file_path
            self.img_info_dic['datetime'] = self.beat()
            collection = Config.get_db_collection(Config.IMAGE_COLLECTION_NAME)
            collection.insert_one(self.img_info_dic)

    @property
    def file_path(self):
        if self.album_name is None:
            folder_path = path.join(Config.ROOT_FOLDER_PATH, self.user_name)
        else:
            folder_path = path.join(Config.ROOT_FOLDER_PATH, self.user_name, self.album_name)
        url_path = urllib.parse.urlparse(self.url_str).path
        if len(url_path) > 0 and url_path[0]=='/':
            url_path = url_path[1:]
        idx_r = url_path.rfind('/')
        if idx_r > 0:
            url_path = url_path[:idx_r]
        url_path = url_path.replace('/', '\\')
        file_path = path.join(folder_path, url_path, self.file_name)
        real_folder_path = path.dirname(file_path)
        if not path.exists(real_folder_path):
            makedirs(real_folder_path)
        return file_path

class DownloadPicThread(Thread):
    def __init__(self, user_name, pange_num_start=4):
        super().__init__(name=user_name)
        self.user_name = user_name
        self.user_page = UserPage.builder(user_name, page_num_start=pange_num_start)
        self.beat()

    def beat(self):
        self._heart_beat_dt = datetime.now()

    def run(self):
        # 加载 用户首界面
        self.user_page.download()

    @property
    def heart_beat_dt(self):
        if self.user_page is not None:
            logger.debug('heart_beat_dt')
            heart_beat_dt_max = self.user_page.heart_beat_dt
            if heart_beat_dt_max > self._heart_beat_dt:
                self._heart_beat_dt = heart_beat_dt_max
        return self._heart_beat_dt


if __name__ == "__main__":

    user_name = 'ly2160046'  # sisiwc  ly2160046
    pange_num_start = 9
    client = MongoClient('127.0.0.1', 27017)
    try:
        db_name = 'test'
        db = client[db_name]
        collection_image = db['s8tu:image']
        collection_album = db['s8tu:album']

        # download_pic_by_albums(user_name)
        t = DownloadPicThread(user_name, pange_num_start=pange_num_start)
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
