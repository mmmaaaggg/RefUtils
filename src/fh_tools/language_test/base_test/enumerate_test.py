import string
s = string.ascii_lowercase
e = enumerate(s)
print("type(s):", type(s))
print(s)
print("type(e):", type(e))
print(list(e))
print("list of enumerate(range(10, 0, -1)):", list(enumerate(range(10, 0, -1))))

