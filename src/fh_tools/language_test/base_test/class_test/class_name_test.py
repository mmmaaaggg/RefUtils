import os
import sys
import inspect
if __name__ == '__main__':
    # get pid
    key = sys._getframe().f_code.co_name
    print(key)
    print(os.getpid())
    print(inspect.stack()[0][1])