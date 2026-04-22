# Error Handling
import os

print("=== Error Handling Demo ===")

# Success case
try:
    with open("test.txt", "w") as f:
        f.write("Hello")
    with open("test.txt", "r") as f:
        content = f.read()
    print(f"Success: {content}")
except Exception as e:
    print(f"Error: {e}")
finally:
    print("Cleanup: deleting file")
    os.remove("test.txt")

# Error case
try:
    with open("nonexistent.txt", "r") as f:
        missing = f.read()
except Exception as e:
    print(f"Caught error: {e}")
finally:
    print("Done with error demo")