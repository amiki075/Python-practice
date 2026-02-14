"""
This file demonstrates multiple inheritance in Python.

A child class inherits from two parent classes.
"""

# First parent class
class Father:
    def skills(self):
        """
        Returns father's skills.
        """
        return "Driving, Fishing"


# Second parent class
class Mother:
    def skills(self):
        """
        Returns mother's skills.
        """
        return "Cooking, Painting"


# Child class inheriting from both parents
class Child(Father, Mother):
    def skills(self):
        """
        Overrides skills() and combines both parents' skills.
        """
        return Father.skills(self) + ", " + Mother.skills(self)


# Create object
child = Child()

# Call method
print(child.skills())