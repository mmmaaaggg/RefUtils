#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2018/8/1 8:31
@File    : only_test.py
@contact : mmmaaaggg@163.com
@desc    : 
"""

from cryptocmd import CmcScraper

# initialise scraper without passing time interval
scraper = CmcScraper('XRP')

# data as list of list in a variable
headers, data = scraper.get_data()

# export the data as csv file, you can also pass optional name parameter
scraper.export_csv('xrp_all_time.csv')

# Pandas dataFrame for the same data
df = scraper.get_dataframe()
