import sys, os

print('os.path.abspath(os.curdir)', os.path.abspath(os.curdir))

print('sys.version', sys.version)
def func_invoked():
    funcName = sys._getframe().f_back.f_code.co_name  # 获取调用函数名
    lineNumber = sys._getframe().f_back.f_lineno  # 获取行号

    print('sys._getframe().f_code.co_name', sys._getframe().f_code.co_name)  # 获取当前函数名


def func_caller():
    func_invoked()

print(func_caller.__name__)
func_caller()
