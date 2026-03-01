import re
def exercise9():
    """Solution for Exercise 9"""
    pattern = r'(?<!^)(?=[A-Z])'
    text = "HelloWorldPythonProgramming"
    
    print("Exercise 9: Insert spaces between words starting with capital letters")
    result = re.sub(pattern, ' ', text)
    print(f"  Original: {text}")
    print(f"  Result: {result}")
    print()