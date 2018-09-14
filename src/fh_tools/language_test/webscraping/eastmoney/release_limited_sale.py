# -*- coding: utf-8 -*-
"""
Created on 2018/2/7
@author: MG
"""
import pandas as pd
from selenium import webdriver
import logging

logger = logging.getLogger()
browser = webdriver.Chrome(executable_path=r'd:\Softwares\Chrome\chromedriver.exe')


def try_n_times(times=3, sleep_time=3, logger: logging.Logger=None, exception=Exception):
    """
    尝试最多 times 次，异常捕获记录后继续尝试
    :param times:
    :param sleep_time:
    :param logger: 如果异常需要 log 记录则传入参数
    :param exception: 可用于捕获指定异常，默认 Exception
    :return:
    """
    last_invoked_time = [None]

    def wrap_func(func):

        @functools.wraps(func)
        def try_it(*arg, **kwargs):
            for n in range(1, times+1):
                if sleep_time > 0 and last_invoked_time[0] is not None\
                        and (time.time() - last_invoked_time[0]) < sleep_time:
                    time.sleep(sleep_time - (time.time() - last_invoked_time[0]))

                try:
                    ret_data = func(*arg, **kwargs)
                except exception:
                    if logger is not None:
                        logger.exception("第 %d 次调用 %s(%s, %s) 出错", n, func.__name__, arg, kwargs)
                    continue
                finally:
                    last_invoked_time[0] = time.time()

                break
            else:
                ret_data = None

            return ret_data

        return try_it

    return wrap_func


@try_n_times(10, logger=logger)
def fetch_release_limited_sale(stock_code, output_path):
    """
    从东方财富网站抓取股票解禁数据，参考网址：http://data.eastmoney.com/dxf/q/300182.html
    :param stock_code: 股票代码
    :param output_path: 输出文件路径
    :return: 
    """
    url_str = "http://data.eastmoney.com/dxf/q/%s.html" % stock_code
    browser.get(url_str)
    browser.implicitly_wait(3)
    element_list = browser.find_elements_by_id('td_1')
    table = element_list[0]
    html = table.get_attribute('outerHTML')
    table_df_list = pd.read_html(html)
    if len(table_df_list) > 0:
        table_df = table_df_list[0]
        table_df.to_csv(output_path, index=False)
        print(table_df)


if __name__ == "__main__":
    logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s] %(message)s')
    stock_code = '300182'
    file_path = 'output.csv'
    fetch_release_limited_sale(stock_code, file_path)
    browser.close()
