# -*- coding: utf-8 -*-

import cchardet as chardet

print(chardet.detect('msg'))

print(chardet.detect('m你好g'))

print(chardet.detect('msg'))

print(chardet.detect(str('msg',"utf-8")))

