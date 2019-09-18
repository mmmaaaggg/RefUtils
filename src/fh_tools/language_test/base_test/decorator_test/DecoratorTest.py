def CheckMethod(f):
    print('checked')
    return f


@CheckMethod
def AMethod(name):
    print('run a_foo', name)


# CheckMethod(a_foo)
print('call a_foo')
AMethod('abc')
