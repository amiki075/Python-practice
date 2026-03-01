import re
def exercise2():
    """Solution for Exercise 2"""
    pattern = r'ab{2,3}'
    
    # Test examples
    test_strings = ['a', 'ab', 'abb', 'abbb', 'abbbb']
    
    print("Exercise 2: a followed by two to three b's")
    for s in test_strings:
        if re.fullmatch(pattern, s):
            print(f"  Match: {s}")
    print()