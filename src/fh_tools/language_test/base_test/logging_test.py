import logging
from logging.handlers import RotatingFileHandler

# formatter = logging.Formatter('[%(asctime)s:  %(levelname)s  %(name)s %(message)s')
# file_handle = RotatingFileHandler("app.log",mode='a',maxBytes=5 * 1024 * 1024,backupCount=2,encoding=None,delay=0)
# file_handle.setFormatter(formatter)
# console_handle = logging.StreamHandler()
# console_handle.setFormatter(formatter)
# loger = logging.getLogger()
# loger.setLevel(logging.INFO)
# loger.addHandler(file_handle)
# loger.addHandler(console_handle)
# STR_FORMAT_DATETIME = '%Y-%m-%d'
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s: %(levelname)s [%(name)s:%(funcName)s] %(message)s')

try:
    aaa = {}
    print(aaa[1])
except Exception as e:
    logging.exception('Exception logged:')
print('go on')

loggerA = logging.getLogger('A')
loggerB = logging.getLogger('B')
loggerA.debug("debug msg")
loggerB.debug("debug msg")

print("set A info level, B warning level")
logging.getLogger('A').setLevel(logging.INFO)
logging.getLogger('B').setLevel(logging.WARNING)
loggerA.info("set A info level")
loggerA.debug("debug msg")
loggerA.info("info msg")
loggerA.warning("warning msg")
loggerA.error("error msg")

loggerB.warning("set B warning level")
loggerB.debug("debug msg")
loggerB.info("info msg")
loggerB.warning("warning msg")
loggerB.error("error msg")
