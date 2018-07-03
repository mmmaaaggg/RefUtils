# -*- coding: utf-8 -*-
"""
Created on Tue Jun 20 15:59:05 2017

@author: forise
"""

import tensorflow as tf
import pandas as pd
import numpy as np

from config_fh import get_db_engine
def get_test(df,num_steps): 
    df['HIGH'] = df.HIGH / df.CLOSE[0]
    df['LOW'] = df.LOW / df.CLOSE[0]
    df['CLOSE'] = df.CLOSE / df.CLOSE[0]
    df['MA_5'] = df.CLOSE.rolling(5).mean()
    df['STD']  = df.CLOSE.rolling(5).apply(lambda x:np.std(x,ddof=1))
    df['b_pect'] = (df.CLOSE - df.MA_5) /(2 * df.STD)
    df['pch'] = df.CLOSE.pct_change()
    df['pch_5'] = df.pch.rolling(5).sum()
    df['pch_20'] = df.pch.rolling(20).sum()
    df['std_5'] = df.STD/df.MA_5
    df['SWING'] = (df.HIGH - df.LOW)/df.CLOSE #* (1+df.pch)
    df['ft_5_20'] = df.FREE_TURN.rolling(5).mean() - df.FREE_TURN.rolling(20).mean()
    df['volume_5_20'] =  df.VOLUME.rolling(5).mean() - df.VOLUME.rolling(20).mean()
    df['cMA'] = df.CLOSE.rolling(11).mean()  ## 7 for step=6
    df_test = df[['SWING','b_pect','pch','pch_5','pch_20','std_5','ft_5_20','volume_5_20']]
    df_test = df_test.tail(num_steps)
    df_test = df_test.reset_index(drop = True)
    
    p_features = df_test.shape[1]
    batch_size = 1
    data_x = np.zeros([p_features,1, num_steps])
    for p in range(p_features):
        raw_x = np.array(df_test.iloc[:,p])
        for i in range(batch_size):
            data_x[p][i]  = raw_x[num_steps * i:num_steps * (i + 1)]
    x = data_x[:, :,0 * num_steps:(0 + 1) * num_steps]
    return x


meta_graph_path = r"D:/Downloads/lstm"
lstm_tuple_path = r"D:/Downloads/lstm_tuple.pickle"
num_steps = 10
sql_query = "select * from wind_index_daily where wind_code = '000001.SH' and trade_date < '2017-05-23'"
engine = get_db_engine()
df = pd.read_sql_query(sql_query, engine)
x_test = get_test(df,num_steps)

sess=tf.Session()    
saver = tf.train.import_meta_graph(meta_graph_path+".meta")
saver.restore(sess,meta_graph_path)
trained_state = np.load(lstm_tuple_path)
result = sess.run('Activation/pred_for_test:0',
         feed_dict={'input/input_placeholder:0':x_test,'pre-process/Placeholder:0':trained_state})
print(result)

