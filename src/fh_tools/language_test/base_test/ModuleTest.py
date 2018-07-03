# -*- coding: utf-8 -*-
import inspect

print('globals() before def class:\n', globals())


class aaa:
    def __init__(self):
        print('instance of %s'% self.__class__.__name__)


class bbb(aaa):
    pass


print('globals() after def class:\n', globals())
print('aaa()', aaa())
print('bbb()', bbb())
print('aaa.__name__', aaa.__name__)
print('aaa.__module__', aaa.__module__)
print('dir(aaa)', dir(aaa))
m = inspect.getmodule(aaa)
print('inspect.getmodule(aaa): ', m)
print('dir(m): ', dir(m))
#mi = inspect.getmoduleinfo('D:\\WorkSpaceJee\\PythonUITest\\language_test\\ModuleTest.py')
mi = inspect.getmodulename('D:\\WorkSpaceJee\\PythonUITest\\language_test\\ModuleTest.py')
print('getmoduleinfo:', mi)
print('dir(mi): ', dir(mi))
print('mi._fields: ', mi._fields)

aClass = getattr(m, 'aaa')
print("getattr(m, 'aaa')'s type:", type(aClass))

aObj = new.instance(aClass)
print(aObj)
print("aClass is globals()['aaa'] : ", aClass is globals()['aaa'])

classname = 'datetime.timedelta'


# @staticmethod
def CreateInstance(class_name, *args, **kwargs):
    '''动态创建类的实例。
    [Parameter]
    class_name - 类的全名（包括模块名）
    *args - 类构造器所需要的参数(list)
    *kwargs - 类构造器所需要的参数(dict)
    [Return] 动态创建的类的实例
    [Example]
    class_name = 'knightmade.logging.Logger'
    logger = Activator.createInstance(class_name, 'logname')
    '''
    (module_name, class_name) = class_name.rsplit('.', 1)
    module_meta = __import__(module_name, globals(), locals(), [class_name])
    class_meta = getattr(module_meta, class_name)
    retObj = class_meta(*args, **kwargs)
    return retObj


aObj = CreateInstance(classname, minutes=6)
print(aObj)
