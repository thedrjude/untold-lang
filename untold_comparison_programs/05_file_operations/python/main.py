# File Operations
with open("data.txt", "w") as f:
    f.write("Hello from Python!")
print("File written!")

with open("data.txt", "r") as f:
    content = f.read()
print(f"Content: {content}")

import os
exists = os.path.exists("data.txt")
if exists:
    print("data.txt exists!")

os.remove("data.txt")
print("File deleted!")