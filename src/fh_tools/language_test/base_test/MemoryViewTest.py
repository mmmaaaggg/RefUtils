# -*- coding:utf-8 -*-
aaa = 'abcdefg'
view = memoryview(aaa)
print('view[3:5] %s'%view[3:5].tobytes())
print('view.readonly %s'%view.readonly)

aaa = bytearray('abcdefg')
view = memoryview(aaa)
print('view.readonly %s'%view.readonly)
view[4] = 'z'
print(aaa)
print(view[3:5].tobytes())

#aaa = bytearray(range(500,510)) ## raise ValueError: byte must be in range(0, 256)
aaa = bytearray(list(range(10)))
view = memoryview(aaa)
print('view.readonly %s'%view.readonly)
#view[4] = 32
#print view.tolist()
print(view[3:5].tolist())

