import re
def exercise3():
    """Solution for Exercise 3"""
    pattern = r'[a-z]+_[a-z]+'
    text = "hello_world test_example python_program"
    
    print("Exercise 3: Lowercase letters joined with underscore")
    matches = re.findall(pattern, text)
    print(f"  Found: {matches}")
    print()