"""
This file demonstrates method overriding in Python.

A child class overrides a method from the parent class.
"""

# Parent class
class Animal:
    def speak(self):
        """
        Returns a generic animal sound.
        """
        return "Animal makes a sound"


# Child class
class Dog(Animal):
    def speak(self):
        """
        Overrides the speak() method of Animal class.
        """
        return "Dog says: Woof!"


# Creating objects
animal = Animal()
dog = Dog()

# Calling methods
print(animal.speak())  # Calls parent method
print(dog.speak())     # Calls overridden method