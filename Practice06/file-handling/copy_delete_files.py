import shutil
import os
shutil.copy2("1.txt","2.txt")
if os.path.exists("1.txt"):
    os.remove("1.txt")
else:
    print("The file doesn't exist")

