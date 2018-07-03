# -*- coding: utf-8 -*-
import html.parser
import urllib.request, urllib.parse, urllib.error

urlText = []

#定义HTML解析器

class parseText(html.parser.HTMLParser):

    def handle_data(self, data):
        if data != '\n':
            urlText.append(data)
#创建HTML解析器的实例
lParser = parseText()

#把HTML文件传给解析器

lParser.feed(urllib.request.urlopen( \
"http://docs.python.org/lib/module-HTMLParser.html" \
).read())

lParser.close()

for item in urlText:
    print(item)