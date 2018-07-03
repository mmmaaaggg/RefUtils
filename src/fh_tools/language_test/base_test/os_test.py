import os

folder_path = r'd:\Works\F复华投资\合同、协议\丰润\丰润一期'
file_names = os.listdir(folder_path)
for file_name in file_names:
    file_path = os.path.join(folder_path, file_name)
    # print(file_path)
    if os.path.isdir(file_path):
        print('folder:', file_path)
        continue
    else:
        file_name_net, file_extension = os.path.splitext(file_path)
        print(file_name_net, '|', file_extension)
