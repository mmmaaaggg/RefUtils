#!usr/bin/env python
# -*- coding: utf-8 -*-
import sys
import os
import urllib.request, urllib.error, urllib.parse
import urllib.request, urllib.parse, urllib.error
import http.cookiejar
import xml.etree.ElementTree as ET
import random
from bs4 import BeautifulSoup
import xlwt
from collections import OrderedDict
from datetime import datetime as dtime
import logging
from logging.handlers import TimedRotatingFileHandler

formatter = logging.Formatter('[%(asctime)s:  %(levelname)s  %(name)s %(message)s')
log_file_handler = TimedRotatingFileHandler(filename="app_log.log", when="D", interval=2, backupCount=10)
#log_file_handler.suffix = "%Y-%m-%d_%H-%M.log"
#log_file_handler.extMatch = re.compile(r"^\d{4}-\d{2}-\d{2}_\d{2}-\d{2}.log$")
log_file_handler.setFormatter(formatter)
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger()
logger.addHandler(log_file_handler)

# console_handle = logging.StreamHandler()
# console_handle.setFormatter(formatter)
# logger.addHandler(console_handle)


# -----------------------------------------------------------------------------
# urloper builder
def UrlOpenerBuilder():
    # Enable cookie support for urllib2
    url = r'https://acms.audiclub.cn/'
    cookiejar = http.cookiejar.CookieJar()
    urlopener = urllib.request.build_opener(urllib.request.HTTPCookieProcessor(cookiejar))
    urllib.request.install_opener(urlopener)

    urlopener.addheaders.append(('Referer', url))
    urlopener.addheaders.append(('Accept-Language', 'zh-CN'))
    urlopener.addheaders.append(('Host', 'acms.audiclub.cn'))
    urlopener.addheaders.append(('User-Agent', 'Mozilla/5.0 (compatible; MISE 9.0; Windows NT 6.1); Trident/5.0'))
    urlopener.addheaders.append(('Connection', 'Keep-Alive'))
    return urlopener


# -----------------------------------------------------------------------------

def download_jpg(fileUrl, urlopener):
    """
    Download from fileUrl then save to fileToSave
    Note: the fileUrl must be a valid file
    :param fileUrl: 
    :param urlopener: 
    :return: 
    """
    isDownOk = False
    try:
        if fileUrl:
            filename = r'code.jpg'
            outfile = open(filename, 'wb')
            urlfile = urlopener.open(urllib.request.Request(fileUrl))
            content = urlfile.read()
            outfile.write(content)
            outfile.close()
            os.startfile(filename)
            isDownOK = True
        else:
            logger.info('ERROR: fileUrl is NULL!')
    except:
        isDownOK = False

    return isDownOK


# -----------------------------------------------------------------------------
# Login in www.***.com.cn
def login_website(urlopener, username, password, paramstr):
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
              'backto': r'https://acms.audiclub.cn/admin/memberlist.html?' + paramstr
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


# ------------------------------------------------------------------------------
def get_user_info_dic(filename):
    # Read users from configure file
    users = {}
    for eachLine in open(filename, 'r'):
        info = [w for w in eachLine.strip().split()]
        if len(info) == 2:
            users[info[0]] = info[1]

    return users


def read_conf_file(filename):
    # Read users from configure file
    params = {}
    for eachLine in open(filename, 'r'):
        info = [w for w in eachLine.strip().split()]
        if len(info) == 2:
            params[info[0]] = info[1]
    return params


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
        # try:
        # book = xlwt.Workbook(encoding='utf-8', style_compression=0)
        # sheet = book.add_sheet(u'客户记录', cell_overwrite_ok=True)

    # rowcount = -1
    for tr in tableobj.find_all('tr'):
        record = [''] * 60
        # rowcount += 1
        colcount = -1
        # ths = tr.find_all('th')
        # if len(ths) > 0:
        #     keystr = 'title'
        #     if keystr in dataset:
        #         continue
        #     for td in ths:
        #         colcount += 1
        #         if colcount == 0:
        #             record[colcount]='ID'
        #         #sheet.write(rowcount, colcount, td.string.strip())
        #         record[colcount]=td.string.strip()
        # else:
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
    # finally:
    #     book.save(u'客户记录.xls')
    return dataset, available


def save_excel(dataset, username):

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
        book.save('客户记录 %s.xls' % username)


# ------------------------------------------------------------------------------
def goto_url(urlopener, url):
    # 跳转的制定页面，并获取html字符串
    urlcontent = urlopener.open(urllib.request.Request(url))
    htmlstr = urlcontent.read(500000)
    return htmlstr


def get_content(contents):
    if len(contents) == 0:
        return ''
    else:
        return contents[0]


# ------------------------------------------------------------------------------
def fetch_data_member_info(htmlstr, record, basepos=12):
    # 获取用户信息页面信息补充到 dataset
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
    # labelobjs=soup.find_all('label')
    # for labelobj in labelobjs:
    # contents = labelobj.contents
    # contentcount = len(contents)
    # u'\u59d3' 姓 查找姓名
    # if contentcount == 1 and contents[0].find(u'\u59d3')>=0:
    #     inputobj = labelobj.fetchNextSiblings('input')[0]
    #     datadic['name'] = inputobj.attrs['value']
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
                    record[basepos + recordposdic[key]] = get_content(op.contents)
                    break
    return record


# ------------------------------------------------------------------------------
def fetch_data_car_info(htmlstr, record, basepos=25):
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
        record[basepos + recordposdic[key]] = get_content(objs[pos].contents)
    return record


# ------------------------------------------------------------------------------
def fetch_data_score_info(htmlstr, record, basepos=31):
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
        record[basepos + recordposdic[key]] = get_content(objs[pos].contents)
    return record


# ------------------------------------------------------------------------------
def fetch_data_insurance(htmlstr, record, basepos=42):
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
            record[basepos + recordposdic[key]] = get_content(objs[pos].contents)
    return record


def build_param_str(Params):
    return '&'.join(['='.join([key, pvalue]) for key, pvalue in list(Params.items())])


# ------------------------------------------------------------------------------
def main():
    Users = get_user_info_dic('config.ini')
    Params = read_conf_file('params.ini')
    # pageon=1&menuid=6&leveltwo=18
    Params['pageon'] = '1'
    Params['menuid'] = '6'
    Params['leveltwo'] = '18'
    paramstr = build_param_str(Params)
    # while True:
    for username, password in list(Users.items()):
        # username = '7580130'
        # password = '92330dttgm]'
        for n in range(3):
            urlopener = UrlOpenerBuilder()
            isOK = login_website(urlopener, username, password, paramstr)
            if isOK:
                # print 'Login successfully!'
                break
            elif n >= 3:
                return
            else:
                logger.info('login failed(%d):', n + 1)
        dataset = None
        pageno = 1
        while 1:
            Params['pageon'] = str(pageno)
            paramstr = build_param_str(Params)
            url = r'https://acms.audiclub.cn/admin/memberlist.html?' + paramstr
            htmlstr = goto_url(urlopener, url)
            dataset, available = fetch_data_member_list(htmlstr, appenddataset=dataset)
            # 调试使用，真实环境中注释掉
            # if dataset is not None and len(dataset) >= 30:
            #     break

            if available:
                logger.info('获取第%d页客户列表信息完成', pageno)
                pageno += 1

            else:
                break
        logger.info('获取客户列表信息全部完成')
        
        memberidlist = [memberid for memberid in list(dataset.keys()) if memberid != 'title']
        # https://acms.audiclub.cn/admin/memberinfo.html?menuid=6&leveltwo=18&memberid=55116
        urlhead = r'https://acms.audiclub.cn/admin/memberinfo.html?menuid=6&leveltwo=18&memberid='
        for n_user, memberid in enumerate(memberidlist):
            for n in range(3):
                try:
                    url = urlhead + memberid
                    htmlstr = goto_url(urlopener, url)
                    dataset[memberid] = fetch_data_member_info(htmlstr, dataset[memberid])
                    logger.info('%d) 获取用户:%s 基本信息', n_user, memberid)
                    break
                except Exception as exp:
                    logger.info('memberid:%s try %d %s', memberid, n + 1)
                    logger.info(exp)
        logger.info('获取客户基本信息完成')

        urlhead = r'https://acms.audiclub.cn/admin/membercarinfo.html?menuid=6&leveltwo=18&memberid='
        for memberid in memberidlist:
            for n in range(3):
                try:
                    url = urlhead + memberid
                    htmlstr = goto_url(urlopener, url)
                    dataset[memberid] = fetch_data_car_info(htmlstr, dataset[memberid])
                    logger.info('%d) 获取用户:%s 车辆信息', n_user, memberid)
                    break
                except Exception as exp:
                    logger.exception('memberid:%s try %d %s', memberid, n + 1)
        logger.info('获取车辆信息完成')

        urlhead = r'https://acms.audiclub.cn/admin/memberlevelscoreinfo.html?menuid=6&leveltwo=18&memberid='
        for memberid in memberidlist:
            for n in range(3):
                try:
                    url = urlhead + memberid
                    htmlstr = goto_url(urlopener, url)
                    dataset[memberid] = fetch_data_score_info(htmlstr, dataset[memberid])
                    logger.info('%d) 获取用户:%s 积分信息', n_user, memberid)
                    break
                except Exception as exp:
                    logger.exception('memberid:%s try %d', memberid, n + 1)
        logger.info('获取积分信息完成')

        urlhead = r'https://acms.audiclub.cn/admin/memberinsurance.html?menuid=6&leveltwo=18&memberid='
        for memberid in memberidlist:
            for n in range(3):
                try:
                    url = urlhead + memberid
                    htmlstr = goto_url(urlopener, url)
                    dataset[memberid] = fetch_data_insurance(htmlstr, dataset[memberid])
                    logger.info('%d) 获取用户:%s 保险信息', n_user, memberid)
                    break
                except Exception as exp:
                    logger.exception('memberid:%s try %d', memberid, n + 1)
        logger.info('获取保险信息完成')

        save_excel(dataset, username)
        logger.info('导出文件完成')


# ------------------------------------------------------------------------------


if __name__ == '__main__':

    logger.info(sys.getdefaultencoding())
    main()

    # url = 'acms.audiclub.cn'
    # urlopener = UrlOpenerBuilder(url)
    # imgurl=r'https://acms.audiclub.cn/verifyCode.html'
    # DownloadFile(imgurl, urlopener)

    # filename = 'htmlstr.html'
    # with open(filename) as htmlfile:
    #     htmlstr = htmlfile.read()
    #     dataset = FetchData_memberlist(htmlstr)
    #  
    # filename = 'memberinfo.html'
    # with open(filename) as htmlfile:
    #     htmlstr = htmlfile.read()
    #     dataset['50220'] = FetchData_memberinfo(htmlstr, dataset['50220'])
    # 
    # filename = 'carinfo.html'
    # with open(filename) as htmlfile:
    #     htmlstr = htmlfile.read()
    #     dataset['50220'] = FetchData_carinfo(htmlstr, dataset['50220'])
    # 
    # filename = 'scoreinfo.html'
    # with open(filename) as htmlfile:
    #     htmlstr = htmlfile.read()
    #     dataset['50220'] = FetchData_scoreinfo(htmlstr, dataset['50220'])
    # 
    # filename = 'insurance.html'
    # with open(filename) as htmlfile:
    #     htmlstr = htmlfile.read()
    #     dataset['50220'] = FetchData_insurance(htmlstr, dataset['50220'])
    # 
    # Save2File(dataset, 'username')
