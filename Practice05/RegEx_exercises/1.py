import re
def exercise1():
    """Solution for Exercise 1"""
    pattern = r'ab*'
    
    # Test examples
    test_strings = ['a', 'ab', 'abb', 'abbb', 'b', 'abc']
    
    print("Exercise 1: a followed by zero or more b's")
    for s in test_strings:
        if re.fullmatch(pattern, s):
            print(f"  Match: {s}")
    print()