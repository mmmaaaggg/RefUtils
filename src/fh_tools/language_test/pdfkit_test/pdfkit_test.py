# -*- coding: utf-8 -*-
"""
Created on 2017/10/26
@author: MG
"""

import pdfkit
pdfkit.from_url('http://www.baidu.com', 'out.pdf')
pdfkit.from_file('test.html', 'out.pdf')
pdfkit.from_string('Hello!', 'out.pdf')
