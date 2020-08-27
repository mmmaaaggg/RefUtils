"""
@author  : MG
@Time    : 2020/8/27 14:58
@File    : invoke_r.py
@contact : mmmaaaggg@163.com
@desc    : 用于
"""

import rpy2.robjects as robjects
r = robjects.r
robjects.r['pi']
file_path = r'C:\Users\26559\Downloads\Guo\SortinoFunc.R'
r['source'](file_path)
v = robjects.FloatVector([1.1, 2.2, 3.3, 4.4, 5.5, 6.6])
r['SortinoFunc'](v, 1)

file_path = r'C:\Users\26559\Downloads\Guo\GuoFunc.R'
r['source'](file_path)(v)
r['GuoFunc'](1)
