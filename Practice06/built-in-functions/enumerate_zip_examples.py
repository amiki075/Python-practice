#enumerate and zip
a = list(input().split())
b = list(map(int, input().split()))
for i,val in enumerate(a):
    print(f"{i}: {val}")
combine = list(zip(a,b))
print(combine)

#Demonstrate type checking and conversions
data = 20
if isinstance(data, int):
    print("Variable is an integer")
else:
    print("Not integer")

string_data = "100"
converted_data = int(string_data)
print(type(converted_data))

items = {1, 2, 3}
list_items = list(items)
print(list_items)

