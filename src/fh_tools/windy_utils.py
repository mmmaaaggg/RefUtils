# -*- coding:utf-8 -*-
"""
    万得缓存接口
wsd_cache 对应 w.wsd 函数
wss_cache 对应 w.wss 函数
wset_cache 对应 w.wset 函数
CACHE_ENABLE 可以取消缓存功能（默认为True）
"""
import json
import os
from collections import OrderedDict
import pandas as pd
from fh_tools.fh_utils import clean_datetime_remove_time_data, date_2_str, clean_datetime_remove_ms

WIND_CACHE = {}
WIND_CACHE_REVERSE = {}
WIND_CACHE_COUNT = 0
filename_index = r'index.txt'
CACHE_INDEX_FILE_PATH = None
CACHE_FOLDER_PATH_DIC = {}

# 默认关闭cache
CACHE_ENABLE = False


def wsd_cache(wind, codes='', fields='close', begin_time=None, end_time=None, options=None, cache=True, * arga, **argb) -> pd.DataFrame:
    key_val_dic = OrderedDict()
    key_val_dic['codes'] = codes
    key_val_dic['fields'] = fields
    key_val_dic['beginTime'] = date_2_str(begin_time)
    key_val_dic['endTime'] = date_2_str(end_time)
    key_val_dic['options'] = options
    key_val_dic['arga'] = arga
    key_val_dic['argb'] = argb
    key = json.dumps(key_val_dic)
    # print('key:%s'%key)
    file_path, is_new = get_file_path(key)
    cache = cache and CACHE_ENABLE
    if cache and not is_new and file_path is not None and os.path.exists(file_path):
        print('*', end='')
        ret_df = pd.read_excel(file_path)
    else:
        wsd_data = wind.wsd(codes, fields, beginTime=begin_time, endTime=end_time, options=options, *arga, **argb)
        ret_df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=[clean_datetime_remove_time_data(d) for d in wsd_data.Times]).T
        if wsd_data.ErrorCode != 0:
            print('wsd("%s", "%s") ErrorCode=%d'%(codes, fields, wsd_data.ErrorCode), 'key:', key_val_dic)
            return None
        if cache:
            ret_df.to_excel(file_path)
    return ret_df


def wsi_cache(wind, codes='', fields='close', begin_time=None, end_time=None, options=None, cache=True, * arga, **argb) -> pd.DataFrame:
    key_val_dic = OrderedDict()
    key_val_dic['codes'] = codes
    key_val_dic['fields'] = fields
    key_val_dic['beginTime'] = date_2_str(begin_time)
    key_val_dic['endTime'] = date_2_str(end_time)
    key_val_dic['options'] = options
    key_val_dic['arga'] = arga
    key_val_dic['argb'] = argb
    key = json.dumps(key_val_dic)
    # print('key:%s'%key)
    file_path, is_new = get_file_path(key)
    cache = cache and CACHE_ENABLE
    if cache and not is_new and file_path is not None and os.path.exists(file_path):
        print('*', end='')
        ret_df = pd.read_excel(file_path)
    else:
        wsd_data = wind.wsi(codes, fields, beginTime=begin_time, endTime=end_time, options=options, *arga, **argb)
        ret_df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=[clean_datetime_remove_ms(d) for d in wsd_data.Times]).T
        if wsd_data.ErrorCode != 0:
            print('wsd("%s", "%s") ErrorCode=%d'%(codes, fields, wsd_data.ErrorCode), 'key:', key_val_dic)
            return None
        if cache:
            ret_df.to_excel(file_path)
    return ret_df


def wss_cache(wind, codes='', fields='', options=None, cache=True, *arga, **argb) -> pd.DataFrame:
    key_val_dic = OrderedDict()
    key_val_dic['codes'] = codes
    key_val_dic['fields'] = fields
    key_val_dic['options'] = options
    key_val_dic['arga'] = arga
    key_val_dic['argb'] = argb
    key = json.dumps(key_val_dic)
    # key = json.dumps({'codes':codes, 'fields':fields, 'options':options, 'arga':arga, 'argb':argb})
    file_path, is_new = get_file_path(key)
    # print(os.path.abspath(filepath))
    # print('os.path.exists(filepath) %s'%os.path.exists(filepath))
    cache = cache and CACHE_ENABLE
    if cache and not is_new and file_path is not None and os.path.exists(file_path):
        # print(u'%4d)read %s %s~%s'%(idx, code, datefrm, dateto))
        print('*', end='')
        ret_df = pd.read_excel(file_path)
    else:
        wsd_data = wind.wss(codes, fields, options, *arga, **argb)
        ret_df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Codes).T
        if wsd_data.ErrorCode != 0:
            print('wss(%s, %s) ErrorCode=%d'%(codes, fields, wsd_data.ErrorCode), 'key:', key_val_dic)
            return None
        if cache:
            ret_df.to_excel(file_path)
    return ret_df


def wset_cache(wind, codes='', fields='', options=None, cache=True, *arga, **argb) -> pd.DataFrame:
    
    key_val_dic = OrderedDict()
    key_val_dic['codes'] = codes
    key_val_dic['fields'] = fields
    key_val_dic['options'] = options
    key_val_dic['arga'] = arga
    key_val_dic['argb'] = argb
    key = json.dumps(key_val_dic)
    # key = json.dumps({'codes':codes, 'fields':fields, 'options':options, 'arga':arga, 'argb':argb})
    
    file_path, is_new = get_file_path(key)
    # print('key', key)
    # print(os.path.abspath(file_path))
    # print('os.path.exists(filepath) %s isnew:%s' % (os.path.exists(file_path), is_new))
    cache = cache and CACHE_ENABLE
    if cache and not is_new and file_path is not None and os.path.exists(file_path):
        # print(u'%4d)read %s %s~%s'%(idx, code, datefrm, dateto))
        print('*', end='')
        ret_df = pd.read_excel(file_path)
    else:
        # wsd_data = wind.wset(codes, fields, options=options, *arga, **argb)
        wsd_data = wind.wset(codes, fields, options, *arga, **argb)
        ret_df = pd.DataFrame(wsd_data.Data, index=wsd_data.Fields, columns=wsd_data.Codes).T
        if wsd_data.ErrorCode != 0:
            print('wset(%s, %s) ErrorCode=%d'%(codes, fields, wsd_data.ErrorCode), 'key:', key_val_dic)
            return None
        if cache:
            ret_df.to_excel(file_path)
    return ret_df


def tdays(wind, beginTime=None, endTime=None, options=None, *arga, **argb) -> pd.DataFrame:
    data = wind.tdays(beginTime, endTime, options, *arga, **argb)
    if data.ErrorCode != 0:
        print('tdays(%s, %s, %s) ErrorCode=%d' % (beginTime, endTime, options, data.ErrorCode))
        return None
    elif len(data.Data) == 0:
        print('tdays(%s, %s, %s) no data return' % (beginTime, endTime, options))
        return None
    ret_df = pd.DataFrame({'date': [d.date() for d in data.Data[0]]})
    return ret_df


def get_cache_folder_path(target_folder_name=None):
    global CACHE_FOLDER_PATH_DIC
    if target_folder_name is None:
        target_folder_name = 'WindCache'
    cache_folder_path = None
    if target_folder_name not in CACHE_FOLDER_PATH_DIC:
        print(u'查找数据目录path:', end="")
        parent_folder_path = os.path.abspath(os.curdir)
        par_path = parent_folder_path
        while not os.path.ismount(par_path):
            # print 'parent path = %s'%par_path
            dir_list = os.listdir(par_path)
            for dir_name in dir_list:
                # print d # .strip()
                if dir_name == target_folder_name:
                    cache_folder_path = os.path.join(par_path, dir_name)
                    print('<', cache_folder_path, '>')
                    break
            if cache_folder_path is not None:
                break
            par_path = os.path.abspath(os.path.join(par_path, os.path.pardir))
        if cache_folder_path is None:
            cache_folder_path = os.path.abspath(os.path.join(parent_folder_path, target_folder_name))
            print('<', cache_folder_path, '> 创建缓存目录')
            os.makedirs(cache_folder_path)
        CACHE_FOLDER_PATH_DIC[target_folder_name] = cache_folder_path
    else:
        cache_folder_path = CACHE_FOLDER_PATH_DIC[target_folder_name]
    return cache_folder_path


def load_cache():
    global WIND_CACHE, WIND_CACHE_COUNT, CACHE_INDEX_FILE_PATH, WIND_CACHE_REVERSE
    cache_folder_path = get_cache_folder_path()
    CACHE_INDEX_FILE_PATH = os.path.join(cache_folder_path, filename_index)
    if os.path.exists(CACHE_INDEX_FILE_PATH):
        print(u'加载WIND_CACHE索引文件')
        with open(CACHE_INDEX_FILE_PATH, 'r') as f:
            WIND_CACHE = json.load(f)
            WIND_CACHE_REVERSE = {v: k for k, v in WIND_CACHE.items()}
    if len(WIND_CACHE) > 0:
        WIND_CACHE_COUNT = max(list(WIND_CACHE.values())) + 1
    else:
        WIND_CACHE_COUNT = 1
    print('存在%d个缓存数据' % (WIND_CACHE_COUNT - 1))


def dump_cache():
    global WIND_CACHE, WIND_CACHE_COUNT, CACHE_INDEX_FILE_PATH, WIND_CACHE_REVERSE
    cache_folder_path = get_cache_folder_path()
    CACHE_INDEX_FILE_PATH = os.path.join(cache_folder_path, filename_index)
    # dump 将数据转换为所有语言都识别的字符串并写入文件
    with open(CACHE_INDEX_FILE_PATH, 'w') as f:
        json.dump(WIND_CACHE, f)
    print('WIND_CACHE索引文件已储存到：', CACHE_INDEX_FILE_PATH, '[%d]' % len(WIND_CACHE))


def get_file_path(key):
    # 后续还需增加线程安全相关内容
    global WIND_CACHE, WIND_CACHE_COUNT
    cache_folder_path = get_cache_folder_path()
    cache_folder_path = '' if cache_folder_path is None else cache_folder_path
    is_new = False
    try:
        file_name_num = WIND_CACHE[key]
        # filename = r'%s\%04d.xls'%(cache_folder_path,file_name_num)
        file_path = os.path.join(cache_folder_path, '%04d.xls' % file_name_num)
    except KeyError:
        file_path = os.path.join(cache_folder_path, '%04d.xls' % WIND_CACHE_COUNT)
        WIND_CACHE[key] = WIND_CACHE_COUNT
        WIND_CACHE_COUNT += 1
        is_new = True
    return file_path, is_new


load_cache()

if __name__ == "__main__":
    from WindPy import w
    w.start()
    today = '2017-01-04'
    ret_df = wset_cache(w, "sectorconstituent", "date=%s;sectorid=1000008494000000" % today)
    print('\n', 'test WindPy.w.wset(...) return:', ret_df.shape)
    dump_cache()
