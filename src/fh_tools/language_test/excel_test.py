import xlrd

file_path = r'd:\Downloads\股票多空.xls'
data = xlrd.open_workbook(file_path) # 打开xls文件
name_list = data.sheet_names()
