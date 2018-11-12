# -*- coding: utf-8 -*-
"""
Created on 2017/7/29
@author: MG
"""
import sys
import os
import urllib.request
import urllib.error
import urllib.parse
import http.cookiejar
from bs4 import BeautifulSoup
import xlwt
from collections import OrderedDict
import logging
from logging.handlers import TimedRotatingFileHandler
from threading import Thread, Lock
from configparser import ConfigParser
import time
import ssl

LOCKER = Lock()
is_debug = False
# 全局取消证书验证
ssl._create_default_https_context = ssl._create_unverified_context


def url_opener_builder() -> urllib.request.OpenerDirector:
    """urloper builder"""
    # Enable cookie support for urllib2
    url = r'https://acms.audiclub.cn/'
    cookiejar = http.cookiejar.CookieJar()
    urlopener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
    urllib.request.install_opener(urlopener)

    urlopener.addheaders.append(('Referer', url))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN,zh'))
    urlopener.addheaders.append(('Host', 'acms.audiclub.cn'))
    urlopener.addheaders.append(('User-Agent',
                                 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/61.0.3163.100 Safari/537.36'))
    urlopener.addheaders.append(('Connection', 'Keep-Alive'))
    return urlopener


def download_jpg(fileUrl, urlopener: urllib.request.OpenerDirector):
    """
    Download from fileUrl then save to fileToSave
    Note: the fileUrl must be a valid file
    :param fileUrl: 
    :param urlopener: 
    :return: 
    """
    is_down_ok = False
    try:
        if fileUrl:
            filename = r'code.jpg'
            with open(filename, 'wb') as outfile:
                urlfile = urlopener.open(urllib.request.Request(fileUrl))
                content = urlfile.read()
                outfile.write(content)

            os.startfile(filename)
            is_down_ok = True
        else:
            logger.info('ERROR: fileUrl is NULL!')
    except IOError:
        is_down_ok = False

    return is_down_ok


def login_website(urlopener, username, password, paramstr):
    """Login in www.***.com.cn"""
    url = 'https://acms.audiclub.cn/login.do'
    logger.info('尝试登陆 账号%s' % username)
    imgurl = r'https://acms.audiclub.cn/verifyCode.html'
    download_jpg(imgurl, urlopener)
    authcode = input('请输入验证码:')
    # authcode=VerifyingCodeRecognization(r"https://192.168.0.106/images/code.jpg")
    logger.info('登录验证，等待回应...')

    # Send login/password to the site and get the session cookie
    values = {'username': username,
              'password': password,
              'verifyCode': authcode,
              # 'backto': r'https://acms.audiclub.cn/admin/memberlist.html?' + paramstr
              'backto': "https://acms.audiclub.cn//admin/index.html",
              }
    #
    urlcontent = urlopener.open(urllib.request.Request(url, urllib.parse.urlencode(values).encode(encoding='UTF8')))
    htmlstr = urlcontent.read(500000)

    # Make sure we are logged in, check the returned page content
    soup = BeautifulSoup(htmlstr, "lxml")
    aobj = soup.find_all('a', attrs={'id': 'LOA6'})
    if len(aobj) == 0:
        logger.info('登录失败  username=%s, password=%s and verifyCode=%s' \
                    % (username, '*' * 8, authcode))  # password
        return False
    else:
        return True
        # tableobjs=soup.find_all('a',class_='how table1')


def fetch_data_member_list(htmlstr, appenddataset=None):
    available = False
    soup = BeautifulSoup(htmlstr, "lxml")
    tableobj = soup.find_all('table', class_='how table1')[0]
    if appenddataset is None:
        dataset = OrderedDict()
        dataset['title'] = ['ID', '姓名', '证件类型', '证件号码', '会员卡号', '移动电话', '当前级别', '当前消费积分', '入会时间', '入会渠道', '入会经销商', '地址',
                            '姓 名', '年龄', '生日', '电子邮件', '地址', '电话', '身份证号码', '入会渠道', '性别', '婚否', '学历', '行业', '职位',
                            '车型', '购车日期', '购车指导价', '车辆识别代码', '购车经销商', '车牌号',
                            '初始定级积分', '初始级别', '当前定级积分', '当前级别', '到达当前级别日期', '当前冻结积分', '累计失效积分', '升级所需顶级积分', '年度冻结的定级积分',
                            '年度将失效的定级积分', '是否被降级',
                            '保险公司名称', '保险起始时间', '保险截止时间', '保险单号', '保险费合计', '购买保险时间', '经销商',
                            '', '', '', '', ]
    else:
        dataset = appenddataset

    # rowcount = -1
    for tr in tableobj.find_all('tr'):
        record = [''] * 60
        # rowcount += 1
        colcount = -1
        tds = tr.find_all('td')
        if len(tds) > 0:
            keystr = 'userid'
            for td in tr.find_all('td'):
                colcount += 1
                inputs = td.find_all('input')
                if len(inputs) > 0:
                    keystr = str(inputs[0].attrs['value'])
                    record[colcount] = keystr
                else:
                    record[colcount] = td.string
                    # sheet.write(rowcount, colcount, td.string)
            if keystr not in dataset:
                dataset[keystr] = record
                available = True
    return dataset, available


def save_excel(dataset, *args):
    book = xlwt.Workbook(encoding='utf-8', style_compression=0)
    try:
        sheet = book.add_sheet('客户记录', cell_overwrite_ok=True)

        keys = list(dataset.keys())
        for nrow in range(len(keys)):
            key = keys[nrow]
            record = dataset[key]
            for ncol in range(len(record)):
                data = record[ncol]
                sheet.write(nrow, ncol, data)
    finally:
        name_tail = ' '.join(args)
        book.save('客户记录 %s.xls' % name_tail)


class Downloader(Thread):

    def __init__(self, urlopener, member_id, dataset):
        super().__init__(name=member_id)
        self.urlopener = urlopener
        self.member_id = member_id
        self.dataset = dataset

    @staticmethod
    def build_param_str(params):
        return '&'.join(['='.join([key, pvalue]) for key, pvalue in list(params.items())])

    def goto(self, url):
        return Downloader.goto_url(self.urlopener, url)

    @staticmethod
    def goto_url(urlopener, url):
        # 跳转的制定页面，并获取html字符串
        urlcontent = urlopener.open(urllib.request.Request(url))
        htmlstr = urlcontent.read(500000)
        return htmlstr

    @staticmethod
    def get_content(contents):
        if len(contents) == 0:
            return ''
        else:
            return contents[0]


class UserBaseInfo(Downloader):
    """获取客户基本信息完成"""

    urlhead = r'https://acms.audiclub.cn/admin/memberinfo.html?menuid=6&leveltwo=18&memberid='

    def fetch_data(self, basepos=12):
        # 获取用户信息页面信息补充到 dataset
        url = self.urlhead + self.member_id
        htmlstr = self.goto(url)
        try:
            LOCKER.acquire()
            record = self.dataset[self.member_id]
            recordposdic = {
                'name': 0,
                'age': 1,
                'birthday': 2,
                'email': 3,
                'address': 4,
                'phone': 5,
                'idcard': 6,
                'ruhuiqudao': 7,
                'sex': 8,
                'merrage': 9,
                'education': 0,
                'hangye': 11,
                'zhiwei': 12,
            }
            soup = BeautifulSoup(htmlstr, "lxml")
            inputdic = {
                'name': 1,
                'age': 2,
                'birthday': 3,
                'email': 4,
                'address': 5,
                'phone': 6,
                'idcard': 7,
                'ruhuiqudao': 8,
            }
            objs = soup.find_all('input')
            for key, pos in list(inputdic.items()):
                record[basepos + recordposdic[key]] = objs[pos].attrs['value']
            selectdic = {
                'sex': 0,
                'merrage': 1,
                'education': 2,
                'hangye': 3,
                'zhiwei': 4,
            }
            objs = soup.find_all('select')
            for key, pos in list(selectdic.items()):
                obj = objs[pos]
                options = obj.find_all('option')
                for op in options:
                    if 'selected' in op.attrs:
                        selected = op.attrs['selected']
                        if selected is not None and selected == 'selected':
                            record[basepos + recordposdic[key]] = Downloader.get_content(op.contents)
                            break
            self.dataset[self.member_id] = record
        finally:
            LOCKER.release()

    def run(self):
        for n in range(3):
            try:
                self.fetch_data()
                logger.debug('获取客户 %s 基本信息', self.member_id)
                break
            except Exception as exp:
                logger.exception('memberid:%s try %d', self.member_id, n + 1)
        logger.debug('获取客户 %s 基本信息完成', self.member_id)


class CarInfo(Downloader):
    """获取车辆信息完成"""

    urlhead = r'https://acms.audiclub.cn/admin/membercarinfo.html?menuid=6&leveltwo=18&memberid='

    def fetch_data(self, basepos=25):
        # 获取用户信息页面信息补充到 dataset
        url = self.urlhead + self.member_id
        htmlstr = self.goto(url)
        try:
            LOCKER.acquire()
            record = self.dataset[self.member_id]
            # 获取车辆信息
            recordposdic = {
                'cartype': 0,
                'baydate': 1,
                'price': 2,
                'carid': 3,
                'cartrader': 4,
                'carcode': 5,
            }
            soup = BeautifulSoup(htmlstr, "lxml")
            idic = {
                'cartype': 0,
                'baydate': 1,
                'price': 2,
                'carid': 3,
                'cartrader': 4,
                'carcode': 5,
            }
            objs = soup.find_all('i', attrs={'class': 'textno'})
            objcount = len(objs)
            for key, pos in list(idic.items()):
                if objcount <= pos:
                    continue
                record[basepos + recordposdic[key]] = Downloader.get_content(objs[pos].contents)
            self.dataset[self.member_id] = record
        finally:
            LOCKER.release()

    def run(self):
        for n in range(3):
            try:
                self.fetch_data()
                logger.debug('获取客户 %s 车辆信息', self.member_id)
                break
            except Exception as exp:
                logger.exception('memberid:%s try %d', self.member_id, n + 1)
        logger.debug('获取客户 %s 车辆信息完成', self.member_id)


class ScoreInfo(Downloader):
    """获取积分信息完成"""

    urlhead = r'https://acms.audiclub.cn/admin/memberlevelscoreinfo.html?menuid=6&leveltwo=18&memberid='

    def fetch_data(self, basepos=31):
        # 获取用户信息页面信息补充到 dataset
        url = self.urlhead + self.member_id
        htmlstr = self.goto(url)
        try:
            LOCKER.acquire()
            record = self.dataset[self.member_id]
            # 获取积分信息
            recordposdic = {
                'initscore': 0,
                'initgrade': 1,
                'currscore': 2,
                'currgrade': 3,
                'gradedate': 4,
                'freezescore': 5,
                'sumlossscore': 6,
                'upneedscore': 7,
                'annualfreezescore': 8,
                'annuallossscore': 9,
                'downgrade': 10,
            }
            soup = BeautifulSoup(htmlstr, "lxml")
            idic = {
                'initscore': 0,
                'initgrade': 1,
                'currscore': 2,
                'currgrade': 3,
                'gradedate': 4,
                'freezescore': 5,
                'sumlossscore': 6,
                'upneedscore': 7,
                'annualfreezescore': 8,
                'annuallossscore': 9,
                'downgrade': 10,
            }
            objs = soup.find_all('i', attrs={'class': 'textno'})
            objcount = len(objs)
            for key, pos in list(idic.items()):
                if objcount <= pos:
                    continue
                record[basepos + recordposdic[key]] = Downloader.get_content(objs[pos].contents)
            self.dataset[self.member_id] = record
        finally:
            LOCKER.release()

    def run(self):
        for n in range(3):
            try:
                self.fetch_data()
                logger.debug('获取客户 %s 积分信息', self.member_id)
                break
            except Exception as exp:
                logger.exception('memberid:%s try %d', self.member_id, n + 1)
        logger.debug('获取客户 %s 积分信息完成', self.member_id)


class InsuranceInfo(Downloader):
    """获取保险信息完成"""

    urlhead = r'https://acms.audiclub.cn/admin/memberinsurance.html?menuid=6&leveltwo=18&memberid='

    def fetch_data(self, basepos=42):
        # 获取用户信息页面信息补充到 dataset
        url = self.urlhead + self.member_id
        htmlstr = self.goto(url)
        try:
            LOCKER.acquire()
            record = self.dataset[self.member_id]
            # 获取积分信息
            recordposdic = {
                'instname': 0,
                'startdate': 1,
                'enddate': 2,
                'instcode': 3,
                'instfee': 4,
                'buydate': 5,
                'trader': 6,
            }
            soup = BeautifulSoup(htmlstr, "lxml")
            trdic = {
                'instname': 0,
                'startdate': 1,
                'enddate': 2,
                'instcode': 3,
                'instfee': 4,
                'buydate': 5,
                'trader': 6,
            }
            tableobj = soup.find_all('table', class_='how table1 fl')[0]

            trs = tableobj.find_all('tr')
            if len(trs) > 1:
                tr = trs[1]
                objs = tr.find_all('td')
                objcount = len(objs)
                for key, pos in list(trdic.items()):
                    if objcount <= pos:
                        continue
                    record[basepos + recordposdic[key]] = Downloader.get_content(objs[pos].contents)
            self.dataset[self.member_id] = record
        finally:
            LOCKER.release()

    def run(self):
        for n in range(3):
            try:
                self.fetch_data()
                logger.debug('获取客户 %s 积分信息', self.member_id)
                break
            except Exception as exp:
                logger.exception('memberid:%s try %d', self.member_id, n + 1)
        logger.debug('获取客户 %s 积分信息完成', self.member_id)


def main():
    cf = ConfigParser()
    cf.read('config.ini')
    user_name = cf.get('user', 'user_name')
    user_pwd = cf.get('user', 'user_pwd')
    # Users = get_user_info_dic('config.ini')
    # Params = read_conf_file('params.ini')
    # pageon=1&menuid=6&leveltwo=18
    section_name = 'start_item_info'
    params = {item: cf.get(section_name, item) for item in cf.options(section_name)}
    # Params['pageon'] = '1'
    # Params['menuid'] = '6'
    # Params['leveltwo'] = '18'
    paramstr = Downloader.build_param_str(params)
    # username = '7580130'
    # password = '92330dttgm]'
    # 登录网站，保留token 信息
    for n in range(3):
        urlopener = url_opener_builder()
        isOK = login_website(urlopener, user_name, user_pwd, paramstr)
        if isOK:
            # print 'Login successfully!'
            break
        elif n >= 3:
            return
        else:
            logger.info('login failed(%d):', n + 1)

    # 加载用户列表
    # dataset = {}
    # user_list = UserList(urlopener, 0, 0, None)
    # user_list.start()
    # user_list.join()
    # user_list.run()
    dataset = None
    pageno = 1
    while 1:
        params['pageon'] = str(pageno)
        paramstr = Downloader.build_param_str(params)
        url = r'https://acms.audiclub.cn/admin/memberlist.html?' + paramstr
        htmlstr = Downloader.goto_url(urlopener, url)
        dataset, available = fetch_data_member_list(htmlstr, appenddataset=dataset)
        # 调试使用，真实环境中注释掉
        if is_debug and dataset is not None and len(dataset) >= 30:
            break

        if available:
            logger.info('获取第%d页客户列表信息完成', pageno)
            pageno += 1
        else:
            break
    logger.info('获取客户列表信息全部完成')
    timeout_second = 60.0
    memberidlist = [memberid for memberid in list(dataset.keys()) if memberid != 'title']
    member_count = len(memberidlist)
    try:
        for n_member, member_id in enumerate(memberidlist):
            # 获取用户基本信息
            logger.info('%d/%d) 获取客户 %s 基本信息、车辆信息、积分信息、保险信息', n_member + 1, member_count, member_id)
            # https://acms.audiclub.cn/admin/memberinfo.html?menuid=6&leveltwo=18&memberid=55116
            user_base_info = UserBaseInfo(urlopener, member_id, dataset)
            user_base_info.start()
            # user_base_info.run()
            car_info = CarInfo(urlopener, member_id, dataset)
            car_info.start()
            score_info = ScoreInfo(urlopener, member_id, dataset)
            score_info.start()
            insurance_info = InsuranceInfo(urlopener, member_id, dataset)
            insurance_info.start()
            # join
            user_base_info.join(timeout_second)
            if user_base_info.is_alive():
                logger.warning('客户 %s 基本信息下载出错，跳过', member_id)
                continue
            car_info.join(timeout_second)
            if car_info.is_alive():
                logger.warning('客户 %s 车辆信息下载出错，跳过', member_id)
                continue
            score_info.join(timeout_second)
            if score_info.is_alive():
                logger.warning('客户 %s 积分信息下载出错，跳过', member_id)
                continue
            insurance_info.join(timeout_second)
            if insurance_info.is_alive():
                logger.warning('客户 %s 保险信息下载出错，跳过', member_id)
                continue
            # 调试使用，真实环境中注释掉
            if is_debug and n_member > 30:
                break
    finally:
        time.sleep(10)
        if dataset is not None:
            save_excel(dataset, user_name, params['startjointime'], params['endjointime'])
            logger.info('导出文件完成')
        else:
            logger.warning('没有数据可导出')


if __name__ == '__main__':
    format_str = '%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s'
    # formatter = logging.Formatter(format_str)
    logging.basicConfig(level=logging.DEBUG, format=format_str)
    log_file_handler = TimedRotatingFileHandler(filename="app_log.log", when="D", interval=2, backupCount=10)
    # log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
    # log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
    # log_file_handler.setFormatter(formatter)
    logging.basicConfig(level=logging.INFO)
    logger = logging.getLogger()
    logger.addHandler(log_file_handler)
    logger.info(sys.getdefaultencoding())
    main()
