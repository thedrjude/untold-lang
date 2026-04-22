// Variables & Data Types
let name = "Untold";
console.log("Name: " + name);

let version: number = 2.1;
console.log("Version: " + version);

let isAwesome: boolean = true;
if (isAwesome) {
    console.log("Untold is awesome!");
}

const PI = 3.14159;
console.log("PI: " + PI);

let numbers = [1, 2, 3, 4, 5];
console.log("Numbers: " + numbers);
console.log("Count: " + numbers.length);

let data = {name: "Untold", version: "2.1"};
console.log("Data: " + JSON.stringify(data));
console.log("Get name: " + data.name);