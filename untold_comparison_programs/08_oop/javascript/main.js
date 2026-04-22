// Classes and Objects (OOP)
class Person {
    constructor(name, age) {
        this.name = name;
        this.age = age;
    }

    greet() {
        console.log(`Hi, I am ${this.name} and I'm ${this.age} years old!`);
    }
}

class Developer extends Person {
    constructor(name, age, language) {
        super(name, age);
        this.language = language;
    }

    introduce() {
        console.log(`I code in ${this.language}`);
    }
}

// Create person object
const p = new Person("Untold", 2);
p.greet();

// Modify properties
p.age = 3;
console.log(`Updated age: ${p.age}`);

// Use inherited behavior
const dev = new Developer("Dev", 25, "JavaScript");
dev.greet();
dev.introduce();