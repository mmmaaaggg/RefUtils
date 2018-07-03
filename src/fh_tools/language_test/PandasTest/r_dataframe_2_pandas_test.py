from rpy2.robjects.vectors import DataFrame as r_DataFrame
import pandas.rpy.common as com
r_df = r_DataFrame({'a': 1, 'b': 2})
print("r_df:\n", r_df)

import pandas as pd
py_df = pd.DataFrame({col:list(l_data) for col, l_data in r_df.items()})

