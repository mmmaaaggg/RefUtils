list1 = ['a', 'b', 'c']
list2 = [1, 2, 3]
zip_list = zip(list1, list2)
tuple_list = [a for a in zip_list]
print("zip(['a', 'b', 'c'], [1, 2, 3]):\n", tuple_list)

lista, listb = zip(*tuple_list)
print("zip(*[('a', 1), ('b', 2), ('c', 3)]):\n", lista, listb)
