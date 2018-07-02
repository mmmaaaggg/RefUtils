## 复华公共函数库

#### windy_utils.py 
调用方式：

    from fh_tools import windy_utils

万得接口的封装函数，主要对WSD、WSS、WSET接口增加了缓存机制
重复接口调用的情况下，接口会自动使用本地缓存进行调用

<b>dump_cache</b> 调用以上函数结束后通过dump_cache()方法将缓存索引文件写入目录，否则缓存将会失效

CACHE_ENABLE 可以取消缓存功能（默认为True）

wsd_cache 对应 w.wsd 函数，返回 DataFrame 对象

wss_cache 对应 w.wss 函数，返回 DataFrame 对象

wset_cache 对应 w.wset 函数，返回 DataFrame 对象

---
#### windy_utils_rest.py
调用方式：

    from fh_tools.windy_utils_rest import WindRest
    WIND_REST_URL = "http://10.0.3.110:5000/wind/"
    wind = WindRest(WIND_REST_URL)

实例化 wind_rest 对象，传入参数为对应rest url地址

对应的wind函数方法包括：

    date_str = wind.tdaysoffset(1, '2017-3-31')
    data_df = wind.wsd("600123.SH", "close,pct_chg", "2017-01-04", "2017-02-28", "PriceAdj=F")
    data_df = wind.wset(table_name="sectorconstituent", options="date=2017-03-21;sectorid=1000023121000000")
    data_df = wind.wss(codes="QHZG160525.OF", fields="fund_setupdate,fund_mgrcomp,fund_existingyear,fund_fundmanager")

---
#### wind_rest_service.py
调用方式：

    from fh_tools.wind_rest_service import start_service
    start_service()

用于启动wind rest服务，启动方法：

---
#### fh_utils.py 
调用方式：

    from fh_tools import fh_utils

各种常用函数
目前由于数量不多，尚未统一整理，大家根据自己喜好使用吧

---
#### ts_utils.py 
调用方式：

    from fh_tools import ts_utils

tushare相关接口封装函数 

---
#### win32_utils.py
调用方式：

    from fh_tools import win32_utils


---

#### language_test
各种测试语句
以各种常用工具包作为目录，对相关函数及数据结构进行一些测试语句编写
很多代码基于python 2.7的代码，稍后会慢慢调整，大家引用的时候看关键语句即可，print语句大部分都是用的2.7的语法

---
## 安装包制作

    python setup.py build     # 编译
    python setup.py install     #安装
    python setup.py sdist       #生成压缩包(zip/tar.gz)
    python setup.py bdist_wininst   #生成NT平台安装包(.exe)
    python setup.py bdist_rpm #生成rpm包
    python setup.py bdist_wheel # 生成wheel包

## 包安装
运行 build_and_install.bat脚本完成工具包编译安装全部过程

    build_and_install.bat
    
