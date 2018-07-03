class A:
    def __init__(self):
        print("Enter A")
        print(super())
        super().__init__()
        print("Leave A")


class B(A):
    def __init__(self):
        print("Enter B")
        print(super())
        super().__init__()
        print("Leave B")


# single = B()
# print(B.mro())
class C(A):
    def __init__(self):
        print("Enter C")
        print(super())
        super().__init__()
        print("Leave C")


class D(B, C):
    def __init__(self):
        print("Enter D")
        print(super())
        super().__init__()
        print("Leave D")


D()
print(D.mro())
