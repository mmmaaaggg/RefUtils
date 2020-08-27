import numpy as np

x = np.array([0, 1, 2, 3, 0, 4, 7, 10])
np.where(np.isin(x, [0,1]))
np.where((x == 0) | (x == 2))




x = np.ones((2, 3))
y = np.zeros((2, 4))
np.concatenate([x, y], axis=1)

x = np.ones((3, 2))
y = np.zeros((4, 2))
np.concatenate([x, y], axis=0)
