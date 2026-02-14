#A Class is like an object constructor, or a "blueprint" for creating objects.
class MyClass:
  x = 5
lass Person:
  def __init__(self, name, age):
    self.name = name
    self.age = age

p1 = Person("Emil", 36)

print(p1.name)
print(p1.age)