# -*- coding: utf-8 -*-
"""
Created on 2017/7/2
@author: MG
"""
from urllib.request import urlopen
from urllib.error import HTTPError
from http.client import IncompleteRead
from bs4 import BeautifulSoup as bs
from os import path, makedirs
from datetime import datetime, timedelta
import time
import logging
import numpy as np
from pymongo import MongoClient
from threading import Thread
logger = logging.getLogger()
max_try_count = 10
ROOT_FOLDER_PATH = r'd:\Downloads\other'
heart_beat_dt = datetime.now()


def download_pic_by_albums(user_name):
    """
    按照 album 进行分类下载
    :param user_name: 
    :return: 
    """
    # http://www.s8tu.com/ly2160046/albums
    # http://www.s8tu.com/ly2160046/?list=images&sort=date_desc&page=2
    logger.info('加载：%s 的相册', user_name)

    # with urlopen("http://www.s8tu.com/%s/albums" % user_name) as rsp:
    #     html_str = rsp.read().decode('utf-8')
    for page_num in np.arange(4, 500, 4):
        try:
            if page_num == 0:
                url_str = "http://www.s8tu.com/%s/albums" % user_name
            else:
                url_str = "http://www.s8tu.com/%s/albums/?sort=date_asc&page=%d" % (user_name, page_num)
            logger.info('加载：相册列表页面，第%d页 %s', page_num, url_str)
            with urlopen(url_str) as rsp:
                html_str = rsp.read().decode('utf-8')
            heart_beat_dt = datetime.now()
        except HTTPError as exp:
            if exp.code == 500:
                logger.info('已经到结尾页')
            else:
                logger.exception('加载：相册列表页面，第%d页 %s 错误', page_num, url_str)
            break
        bsobj = bs(html_str, "lxml")
        link_list = bsobj.findAll("a", {"data-text": "album-name"})
        link_count = len(link_list)
        all_failed_albums = True
        for n, link in enumerate(link_list):
            album_url = link['href']
            logger.info('加载第%d页：%s 的相册[%d/%d]', page_num, user_name, n + 1, link_count)
            link_count_sub, success_count = download_pic_from_album(album_url)
            if link_count_sub == success_count or success_count > 0:
                all_failed_albums = False
        # 加入相册全部都失败，则退出循环
        if all_failed_albums:
            logging.error('加载：相册列表页面，第%d页 %s 全部失败', page_num, url_str)
            break


def check_done(collection, url_str, key='url', true_action=None):
    """检查集合中是否存在当前url"""
    content = collection.find_one({key: url_str})
    is_exist = content is not None
    if is_exist:
        if true_action is not None:
            true_action(content)
        logger.debug('%s %s:%s 已经被下载过了', collection.name, key, url_str)
    heart_beat_dt = datetime.now()
    return is_exist


def check_all_done(collection, url_str, key='url', true_action=None):
    """检查是否当前相册以及被下载 0 未下载 1 已下载 2 全部已下载"""
    content = collection.find_one({key: url_str})
    ret_status = 1 if content is not None else 0
    link_count, image_count = 0, 0
    if ret_status != 0 and 'tot_image_count' in content:
        link_count = content['image_count']
        image_count = content['tot_image_count']
        ret_status = 2 if link_count == image_count else ret_status
        if ret_status == 2:
            logger.debug('%s %s:%s 全部相册内容均已经被下载', collection.name, key, url_str)
        elif ret_status == 1:
            logger.debug('%s %s:%s 已经被下载过了', collection.name, key, url_str)
    heart_beat_dt = datetime.now()
    return ret_status, link_count, image_count


def download_pic_from_album(album_url):
    """
    加载相册url里面内容，下载全部图片
    :param album_url: 
    :return: 
    """
    # http://www.s8tu.com/album/xq
    # http://www.s8tu.com/album/xq/?sort=date_asc&page=2
    for page_num in np.arange(2, 500, 2):
        if page_num == 0:
            album_url_page = album_url
        else:
            album_url_page = album_url + '/?sort=date_asc&page=%d' % page_num
        ret_status, link_count, image_count = check_all_done(collection_album, album_url_page)
        success_count = link_count
        if ret_status == 1:
            continue
        elif ret_status == 2:
            break
        global max_try_count
        try:
            logger.info('加载：图片列表页，第%d页 %s', page_num, album_url_page)
            with urlopen(album_url_page) as rsp:
                html_str = rsp.read().decode('utf-8')
                time.sleep(0.1)
        except HTTPError as exp:
            if exp.code == 500:
                logger.info('已经到图片列表页结尾')
            else:
                logger.exception()
            break

        bsobj = bs(html_str, "lxml")
        image_count_str = bsobj.find("b", {"data-text": "image-count"}).contents[0]
        image_count = int(image_count_str)
        link_list = bsobj.findAll("a", {"class": "image-container"})
        link_count = len(link_list)
        success_count = 0
        for n, link in enumerate(link_list):
            image_page_url = link['href']
            logger.info('加载：图片页[%d/%d/%d] %s', n + 1, link_count, image_count, image_page_url)
            try_count = 0
            for try_count in range(max_try_count):
                try:
                    download_pic_from_page(image_page_url)
                    success_count += 1
                    break
                except:
                    logger.exception('加载：图片页%s 失败[%d/%d]', image_page_url, try_count, max_try_count)
                    time.sleep(2 ** try_count)
            else:
                logger.error('图片下载失败[%d/%d/%d]：%s', n, link_count, image_count, image_page_url)
                all_success = False
        if success_count == link_count:
            dic = {'url': album_url_page,
                   'image_count': link_count,
                   'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
                   'tot_image_count': image_count,
                   }
            collection_album.insert_one(dic)
        if image_count == link_count:
            break
        time.sleep(0.1)
    return link_count, success_count


def download_pic_from_page(image_page_url):
    """
    从图片页面，通过下载按钮下载图片文件
    :param image_page_url: 
    :return: 
    """
    if check_done(collection_image, image_page_url, key='image_page_url'):
        return
    try:
        with urlopen(image_page_url) as rsp:
            html_str = rsp.read().decode('utf-8')
    except IncompleteRead:
        logger.exception('加载：图片页 %s 失败', image_page_url)
        return
    bsobj = bs(html_str, "lxml")
    link = bsobj.find("a", {"rel": "tooltip"})
    image_url = link['href']
    key = 'url'

    def update_key(content):
        """临时使用"""
        content['image_page_url'] = image_page_url
        collection_image.update_one({key: image_url}, {'$set': content})
        logger.info('update {%s: %s} to\n%s', key, image_url, content)

    if check_done(collection_image, image_url, key=key,
                  true_action=update_key):
        heart_beat_dt = datetime.now()
        return
    file_name = link['download']
    p_folder_name_user_name = bsobj.find('a', {"class": "user-link"}).contents[0]
    p_folder_name_album_name = bsobj.find('meta', {"name": "description"})['content']
    try:
        idx_start = p_folder_name_album_name.find('在')
        idx_end = p_folder_name_album_name.find('相册')
        p_folder_name_album_name = p_folder_name_album_name[idx_start + 1:idx_end].strip()
    except:
        pass
    bsobj_tag = bsobj.find('a', {"href": image_page_url})
    global ROOT_FOLDER_PATH
    folder_path = path.join(ROOT_FOLDER_PATH, p_folder_name_user_name, p_folder_name_album_name)
    if not path.exists(folder_path):
        makedirs(folder_path)
    file_path = path.join(folder_path, file_name)
    logger.debug('图片保存到：%s\n来源网址：%s', file_path, image_url)
    with urlopen(image_url) as rsp:
        content = rsp.read()
    with open(file_path, mode='wb') as output:
        output.write(content)
    dic = {'image_page_url': image_page_url,
           'url': image_url,
           'file_path': file_path,
           'datetime': datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
    collection_image.insert_one(dic)
    heart_beat_dt = datetime.now()


class DownloadPicThread(Thread):

    def __init__(self, user_name):
        super().__init__(name=user_name)
        self.user_name = user_name

    def run(self):
        download_pic_by_albums(user_name)

if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG,
                        format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')
    user_name = 'ly2160046'  # sisiwc  ly2160046
    client = MongoClient('127.0.0.1', 27017)
    try:
        db_name = 'test'
        db = client[db_name]
        collection_image = db['s8tu:image']
        collection_album = db['s8tu:album']

        #download_pic_by_albums(user_name)
        t = DownloadPicThread(user_name)
        t.start()
        while 1:
            time.sleep(10)
            if t.is_alive() and datetime.now() - heart_beat_dt < timedelta(minutes=3):
                continue
            t.join(1)
            logger.warning('重启线程')
            heart_beat_dt = datetime.now()
            t = DownloadPicThread(user_name)
            t.start()
        # 相册下载测试
        # album_url_str = 'http://www.s8tu.com/album/xq'
        # download_pic_from_album(album_url_str)
    finally:
        client.close()
