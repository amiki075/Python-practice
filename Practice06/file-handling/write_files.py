with open("1.txt",'a') as f:
    f.write("Now the file has more content!")

with open("1.txt",'r') as f:
    print(f.read())