import pandas as pd
import numpy as np
import pandas.util.testing as tm

def unpivot(frame):
    N, K = frame.shape
    print('frame.shape', N, K)
    data = {'value' : frame.values.ravel('F'),
            'variable' : np.asarray(frame.columns).repeat(N),
            'date' : np.tile(np.asarray(frame.index), K)}
    return pd.DataFrame(data, columns=['date', 'variable', 'value'])

tm.N = 3
df = unpivot(tm.makeTimeDataFrame())
print(df)
df_pivot = df.pivot(index='date', columns='variable', values='value')
print(df_pivot)
