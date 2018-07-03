# -*- coding: utf-8 -*-
from collections import OrderedDict

k1 = 'asdf'
aaa = dict()
print('k1 in aaa %s'% (k1 in aaa))

aaa['a'] = list(range(3))
aaa['b'] = list(range(4))
aaa['c'] = list(range(5))
aaa['d'] = list(range(6))

print('d is in key:', 'd' in aaa)

for k, v in list(aaa.items()):
    print(k, v)
aaa.pop('a')
print('aaa.pop(''a'')  aaa = ', aaa)
del aaa['b']
print("del aaa['b'] aaa = ", aaa)

print('last one')
print([(key, aaa[key][-1]) for key in aaa if aaa[key][1] != 0])
aaa.clear()

aaa.update()

print('collections.OrderedDict')
aaa['c'] = 'C'
aaa['f'] = 'F'
aaa['d'] = 'D'
aaa['b'] = 'B'
print('aaa.keys() %s'%list(aaa.keys()))
print('OrderedDict(aaa) %s'%OrderedDict(aaa))
aaaSorted = sorted(aaa) 
print('sorted(aaa.items()) %s'%sorted(aaa.items()))
odic = OrderedDict(sorted(aaa.items()))
print('OrderedDict(sorted(aaa.items())) %s'%odic)
odic['a'] = 'A'
print('odic[''a''] = ''A'' %s'%odic)
print('sorted(odic.items()) %s'%sorted(odic.items()))

try:
    odic['adsf']
except KeyError:
    print("odic['adsf'] except: KeyError")

# ————————————————————————————————————
print("tuple key test")
aaa = {}
aaa[('abc', 123)] = 'abc,123'
if ('abc', 123) in aaa:
    print("('abc', 123) in dic")


def extent_dic(**kwargs):
    aaa = {'a': 1}
    print('aaa:', aaa)
    aaa.update(kwargs)
    print('after aaa.update(kwargs):', aaa)

extent_dic()

extent_dic(abc=123, defg=4567)
