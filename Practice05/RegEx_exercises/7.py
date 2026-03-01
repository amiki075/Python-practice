import re
def exercise7():
    """Solution for Exercise 7"""
    def snake_to_camel(snake_str):
        components = snake_str.split('_')
        return components[0] + ''.join(x.title() for x in components[1:])
    
    text = "hello_world_python_programming"
    
    print("Exercise 7: Snake case to camel case")
    result = snake_to_camel(text)
    print(f"  Original: {text}")
    print(f"  Result: {result}")
    print()