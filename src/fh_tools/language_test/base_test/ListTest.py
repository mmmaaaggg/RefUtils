print("[0]*10:", ['']*10)
aaa = list(range(5))
print(("aaa = range(5) :", aaa))
aaa = list(range(5))
print(("aaa = list(range(5)) :", aaa))
aaa.extend(list(range(5, 0, -1)))
print(('aaa.extend(range(5, 0, -1))', aaa))

aaa.append(None)
print(('aaa.append(6):%s'%aaa.append(6)))
print(('aaa after append:%s'%aaa))

print(('aaa.pop(6) =%d'%aaa.pop(6)))
print(('aaa :', aaa))

print(("aaa.index(1)", aaa.index(1)))
print(('aaa.index(2, 5)', aaa.index(2, 5)))

aaa = [3, 4, 2, 6, 8 ,7 , 1, 0]
print(('aaa unsorted:%s' % aaa))
aaa.sort()
print(('aaa after sort():%s' % aaa))

