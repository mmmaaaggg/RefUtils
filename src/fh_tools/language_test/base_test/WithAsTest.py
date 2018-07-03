# -*- coding: utf-8 -*-

class WithTest:
    
    def __enter__(self):
        print('enter')
    
    def __exit__(self, exc_type, exc_value, traceback):
        print(('exit exc_type=%s\nexc_value=%s\ntraceback=%s\n'%(exc_type, exc_value, traceback)))

with WithTest() as wt:
    print('do somthine')
    raise Exception()
print('end')