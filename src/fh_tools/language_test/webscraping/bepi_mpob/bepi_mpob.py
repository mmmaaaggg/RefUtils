#! /usr/bin/env python
# -*- coding:utf-8 -*-
"""
@author  : MG
@Time    : 2019/1/4 10:45
@File    : bepi_mpob.py
@contact : mmmaaaggg@163.com
@desc    : 
"""
import requests
import pandas as pd
url = "http://bepi.mpob.gov.my/admin2/price_ffb_region_view2.php"

# tahun: 2018
# bulan: 10
# Submit2: View Price

res = requests.post(url, data={"tahun": 2018, "bulan": 10, "Submit2": "View+Price"})
df = pd.read_html(res.content, header=[5], index_col=[0])[0]

print(df)
