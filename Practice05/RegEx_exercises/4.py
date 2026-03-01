import re
def exercise4():
    """Solution for Exercise 4"""
    pattern = r'[A-Z][a-z]+'
    text = "Hello World Python Programming TEST"
    
    print("Exercise 4: One uppercase followed by lowercase letters")
    matches = re.findall(pattern, text)
    print(f"  Found: {matches}")
    print()