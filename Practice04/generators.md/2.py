def even_numbers(n):
    for i in range(0, n + 1, 2):
        yield i

n = int(input("Enter n: "))
result = list(even_numbers(n))
print(*result, sep=", ")