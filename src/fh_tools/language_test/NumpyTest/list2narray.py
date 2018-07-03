import numpy as np
listlen = 20
alist = np.array(list(range(listlen)))
matrixwidth = 5
matrixlen = listlen - matrixwidth + 1

amatrix = np.empty((matrixlen, matrixwidth))
for n in range(matrixlen): amatrix[n] = alist[np.arange(n, n+matrixwidth)]

bmatrix = []
for n in range(matrixlen): bmatrix.append(alist[np.arange(n, n+matrixwidth)])

print(amatrix)