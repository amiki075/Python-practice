import re
def exercise5():
    """Solution for Exercise 5"""
    pattern = r'^a.*b$'
    
    # Test examples
    test_strings = ['ab', 'acb', 'a123b', 'a_b', 'a', 'b', 'abc']
    
    print("Exercise 5: a followed by anything, ending in b")
    for s in test_strings:
        if re.match(pattern, s):
            print(f"  Match: {s}")
    print()