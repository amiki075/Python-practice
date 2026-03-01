import re
def exercise6():
    """Solution for Exercise 6"""
    pattern = r'[ ,.]'
    text = "Hello, world. This is a test"
    
    print("Exercise 6: Replace space, comma, or dot with colon")
    result = re.sub(pattern, ':', text)
    print(f"  Original: {text}")
    print(f"  Result: {result}")
    print()