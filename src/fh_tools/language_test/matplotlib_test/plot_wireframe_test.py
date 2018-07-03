'''
===================================
3D wireframe plots in one direction
===================================

Demonstrates that setting rstride or cstride to 0 causes wires to not be
generated in the corresponding direction.
'''

from mpl_toolkits.mplot3d import axes3d
import matplotlib.pyplot as plt
import pandas as pd
import numpy as np


def df_plot(df):
    fig, ax = plt.subplots(subplot_kw=dict(projection='3d'))
    x1 = np.array(df.index)
    y1 = np.array(df.columns)
    xx = np.tile(x1, (len(y1), 1))
    yy = np.tile(y1, (len(x1), 1)).T
    zz = df.as_matrix()
    ax.plot_wireframe(xx, yy, zz, rstride=10, cstride=0)
    plt.tight_layout()
    plt.show()

# fig, [ax1, ax2] = plt.subplots(2, 1, figsize=(8, 12), subplot_kw={'projection': '3d'})


# Get the test data
X, Y, Z = axes3d.get_test_data(0.05)
# print('x:\n', X)
# print('y:\n', Y)
# print('z:\n', Z)
df = pd.DataFrame(Z, index=X[0], columns=Y[:, 0])
df_plot(df)

