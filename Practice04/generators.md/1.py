def squares_up_to(n):
    for i in range(1, n + 1):
        yield i * i

n = int(input("Enter N: "))
for square in squares_up_to(n):
    print(square, end=" ")