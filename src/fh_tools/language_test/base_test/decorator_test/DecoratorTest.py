def CheckMethod(f):
    print('checked')
    return f


@CheckMethod
def AMethod(name):
    print('run AMethod', name)


# CheckMethod(AMethod)
AMethod('abc')
