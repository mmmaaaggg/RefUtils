# -*- coding: utf-8 -*-
"""
Created on 2017/4/11
@author: MG
"""
from WindPy import w
w.start()
data = w.wsq("600007.SH,600006.SH", "rt_time,rt_susp_flag,rt_high_limit,rt_last,rt_trade_status")
w.close()
print(data)
import pandas as pd
df = pd.DataFrame(data.Data, index=data.Fields, columns=data.Codes)
df["600007.SH"]['RT_SUSP_FLAG']
df['RT_HIGH_LIMIT'][0] == s1['RT_LAST'][0]
df['RT_SUSP_FLAG'][0]

