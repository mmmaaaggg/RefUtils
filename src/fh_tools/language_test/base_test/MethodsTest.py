import abc


class StrategyBase:

    def AMethod(self):
        print('a method', self)

    @staticmethod
    def StaticMethod():
        print('static method')

    @classmethod
    def ClassMethod(cls):
        print('class method', cls)

    @abc.abstractmethod
    def AbsMethod(self, Name):
        '''abstract method'''
        print('abstract method param=', self, Name)

StrategyBase.StaticMethod()
StrategyBase.ClassMethod()
stgbase = StrategyBase()
stgbase.AMethod()
stgbase.AbsMethod('Name')

print('---------------------')


class StrategyA(StrategyBase):
    pass

StrategyA.StaticMethod()
StrategyA.ClassMethod()
stg = StrategyA()
stg.AMethod()
stg.AbsMethod('subclass')
