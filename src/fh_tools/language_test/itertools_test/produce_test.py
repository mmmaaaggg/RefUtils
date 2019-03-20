from itertools import product

iter_func = range(3)
iter_result = product(iter_func, repeat=3)
print("product(iter_func, repeat=3)")
for comp in iter_result:
    print(comp)

iter_result = product(range(2), range(3), range(4))
print("product(range(2), range(3), range(4))")
for comp in iter_result:
    print(comp)

