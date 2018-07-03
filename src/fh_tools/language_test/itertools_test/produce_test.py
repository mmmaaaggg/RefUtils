from itertools import product

iter_func = range(3)
iter_result = product(iter_func, repeat=3)
for comp in iter_result:
    print(comp)
