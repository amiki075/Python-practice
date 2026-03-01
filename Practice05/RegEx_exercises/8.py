import re
def exercise8():
    """Solution for Exercise 8"""
    pattern = r'(?=[A-Z])'
    text = "HelloWorldPythonProgramming"
    
    print("Exercise 8: Split at uppercase letters")
    result = re.split(pattern, text)
    print(f"  Original: {text}")
    print(f"  Result: {result}")
    print()