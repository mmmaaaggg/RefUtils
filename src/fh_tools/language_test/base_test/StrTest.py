# -*- coding: utf-8 -*-
aaa = '.'
bbb = aaa.join(['a', 'b', 'c'])

# 字符串分割
print(aaa)
print(bbb)
ccc = bbb.split('.')
print('ccc:', ccc)
index = bbb.rindex('.')
print('bbb.rindex(".") ~: %s %s'%(bbb[:index], bbb[index+1:]))
print("bbb.find('asdf') : %s"%bbb.find('asdf'))
# 字符串链接
print(['asdf_' 'ffff'])

aaa = ['asdf','ghij']
bbb = aaa[0] + aaa[1]
print(bbb)
bbb = aaa[0], aaa[1]
print(bbb)
bbb = '%s-%s' % (aaa[0], aaa[1])
print(bbb)

aaa = bbb.replace('df', 'zy')
print(bbb)
print(aaa)

aaa = 'XT1514599.XT,XT1514860.XT,XT1500302.XT,XT1500671.XT,XT1505384.XT,XT1505856.XT,XT1510063.XT,XT1510069.XT,XT1514597.XT'
bbb = aaa.split(sep=',')
print(bbb)

print("mysql+pymysql://%(DB_USER)s:%(DB_PASSWORD)s@%(DB_IP)s:%(DB_PORT)s/%(DB_NAME)s?charset=utf8" % {
    'DB_USER': 'DB_USER',
    'DB_PASSWORD': 'DB_PASSWORD',
    'DB_IP': 'DB_IP',
    'DB_PORT': 'DB_PORT',
    'DB_NAME': 'DB_NAME'})

class AClass:
    def __init__(self):
        self.property1 = 1
        self.property2 = 'b'

aclass = AClass()
print('{0.__class__.__name__}.property1:{0.property1:d}\n{0.__class__.__name__}.property2:{0.property2:s}'.format(aclass))