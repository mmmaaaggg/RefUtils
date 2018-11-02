# -*- coding: utf-8 -*-
"""
Created on 2018/1/1
@author: MG
"""

class Foo:
    def __init__(self, alist):
        self.alist = alist
        self.adic = {str(aa): aa for aa in alist}

    @property
    def blist(self):
        return self.alist

    @property
    def bdic(self):
        return self.adic


foo = Foo([1,2,3])
print(foo.alist)
print("foo.blist[1]: ", foo.blist[1])
print("foo.bdic['1']: ", foo.bdic['1'])

