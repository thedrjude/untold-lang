# Functions
def add(a, b):
    return a + b

def greet(name, greeting="Hello"):
    return f"{greeting}, {name}!"

result = add(5, 3)
print(f"5 + 3 = {result}")

greeting = greet("Untold")
print(greeting)

square = lambda x: x * x
print(f"Square of 7: {square(7)}")