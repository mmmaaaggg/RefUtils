##pip install pytdx
from pytdx.hq import TdxHq_API

api = TdxHq_API()

api.connect('59.173.18.140', 7709)
print("获取股票行情")

data = api.get_k_data('000002', '2005-07-01', '2017-07-10')

data2 = api.get_xdxr_info(1, '600300')

print(data2)

print("获取股票行情")
stocks = api.get_security_quotes([(0, "000002"), (1, "600300")])

print(stocks)
print("获取k线")
data = api.get_security_bars(9, 0, '000001', 4, 3)
print(data)
print("获取 深市 股票数量")
print(api.get_security_count(0))
print("获取股票列表")
stocks = api.get_security_list(1, 255)
print(stocks)
print("获取指数k线")
data = api.get_index_bars(9, 1, '000001', 1, 2)
print(data)
print("查询分时行情")
data = api.get_minute_time_data(1, '600300')
print(data)
print("查询历史分时行情")
data = api.get_history_minute_time_data(
    1, '600300', 20161209)
print(data)
print("查询分时成交")
data = api.get_transaction_data(1, '000002', 0, 30)
print(data)
print("查询历史分时成交")
data = api.get_history_transaction_data(
    2, '600302', 0, 10, 20170209)
print(data)
print("查询公司信息目录")
data = api.get_company_info_category(1, '000003')
print(data)
print("读取公司信息-最新提示")
data = api.get_company_info_content(0, '000001', '000001.txt', 0, 10)
print(data)
print("读取除权除息信息")
data = api.get_xdxr_info(1, '600300')
print(data)
print("读取财务信息")
data = api.get_finance_info(0, '000001')
print(data)
print("日线级别k线获取函数")
data = api.get_k_data('000001', '2005-07-01', '2017-07-10')
print(data)




