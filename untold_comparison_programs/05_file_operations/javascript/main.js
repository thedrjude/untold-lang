// File Operations
const fs = require('fs');

fs.writeFileSync("data.txt", "Hello from JavaScript!");
console.log("File written!");

const content = fs.readFileSync("data.txt", "utf8");
console.log(`Content: ${content}`);

const exists = fs.existsSync("data.txt");
if (exists) {
    console.log("data.txt exists!");
}

fs.unlinkSync("data.txt");
console.log("File deleted!");