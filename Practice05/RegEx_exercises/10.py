import re
def exercise10():
    """Solution for Exercise 10"""
    def camel_to_snake(camel_str):
        pattern = r'(?<!^)(?=[A-Z])'
        return re.sub(pattern, '_', camel_str).lower()
    
    text = "HelloWorldPythonProgramming"
    
    print("Exercise 10: Camel case to snake case")
    result = camel_to_snake(text)
    print(f"  Original: {text}")
    print(f"  Result: {result}")
    print()