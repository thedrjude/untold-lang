# Classes and Objects (OOP)
class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age

    def greet(self):
        print(f"Hi, I am {self.name} and I'm {self.age} years old!")

class Developer(Person):
    def __init__(self, name, age, language):
        super().__init__(name, age)
        self.language = language

    def introduce(self):
        print(f"I code in {self.language}")

# Create person object
p = Person("Untold", 2)
p.greet()

# Modify properties
p.age = 3
print(f"Updated age: {p.age}")

# Use inherited behavior
dev = Developer("Dev", 25, "Python")
dev.greet()
dev.introduce()