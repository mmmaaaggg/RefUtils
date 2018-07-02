# python setup.py build     # 编译
# python setup.py install     #安装
# python setup.py sdist       #生成压缩包(zip/tar.gz)
# python setup.py bdist_wininst   #生成NT平台安装包(.exe)
# python setup.py bdist_rpm #生成rpm包
from setuptools import setup, find_packages

setup(
    name='ref_utils',
    version=0.1,
    packages=find_packages('src'),  # 包含所有src中的包
    package_dir={'': 'src'},  # 告诉distutils 包在src目录下
    author='MG',
    author_email='mmmaaaggg@163.com',
    url='',
    license='MIT',
    description='Variable utils', install_requires=['arch', 'numpy', 'requests', 'flask_restplus', 'redis', 'pymysql', 'selenium']
)
