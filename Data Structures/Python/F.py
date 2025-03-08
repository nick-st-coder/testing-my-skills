f = open("test.txt", "w")
f.write("hi how are you, is everything okay?")

f = open("test.txt", "r")
print(f.read())

import os

os.remove("test.txt")