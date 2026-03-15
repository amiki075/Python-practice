from functools import reduce
a = list(map(int, input().split()))
f = list(map(lambda x:x**3,a))
d = list(filter(lambda x:x % 2 != 0,a))
q = reduce(lambda x,y:x + y,a)
print(f)
print(d)
print(q)