aaa = set(['a', 'b', 'c'])
print("aaa = set(['a', 'b', 'c']) =", aaa)
bbb = set(['c', 'd', 'e'])
print("bbb = set(['c', 'd', 'e']) =", bbb)

print("aaa.add('g') =", aaa.add('g'))
print("after aaa.add('g') aaa =", aaa)

print("交：aaa & bbb = ", aaa & bbb)
print("并：aaa | bbb = ", aaa | bbb)
print("差：aaa - bbb = ", aaa - bbb)

print("','.join(bbb) = ", ','.join(bbb))

print("集合比较运算", set(['a', 'b', 'c']) == set(['a', 'b', 'c']))
