// Functions
const add = (a, b) => a + b;

const greet = (name, greeting = "Hello") => `${greeting}, ${name}!`;

const result = add(5, 3);
console.log(`5 + 3 = ${result}`);

const greeting = greet("Untold");
console.log(greeting);

const square = (x) => x * x;
console.log(`Square of 7: ${square(7)}`);