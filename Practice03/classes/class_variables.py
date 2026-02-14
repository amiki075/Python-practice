# Example: Demonstrating class variables vs instance variables
class Student:
    # Class variable (shared by all objects)
    school_name = "International High School"

    def __init__(self, name, grade):
        # Instance variables (unique for each object)
        self.name = name
        self.grade = grade

    def display_info(self):
        print(f"Name: {self.name}")
        print(f"Grade: {self.grade}")
        print(f"School: {Student.school_name}")
        print("-------------------------")


# Creating objects
student1 = Student("Amir", 10)
student2 = Student("Sara", 11)

# Display information before changing class variable
print("Before changing school name:")
student1.display_info()
student2.display_info()

# Changing class variable
Student.school_name = "Global Academy"

# Display information after changing class variable
print("After changing school name:")
student1.display_info()
student2.display_info()

# Changing instance variable only for one object
student1.grade = 12

print("After changing student1's grade:")
student1.display_info()
student2.display_info()