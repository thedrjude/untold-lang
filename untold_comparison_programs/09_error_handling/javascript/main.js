// Error Handling
const fs = require('fs');

console.log("=== Error Handling Demo ===");

// Success case
try {
    fs.writeFileSync("test.txt", "Hello");
    const content = fs.readFileSync("test.txt", "utf8");
    console.log(`Success: ${content}`);
} catch (err) {
    console.log(`Error: ${err.message}`);
} finally {
    console.log("Cleanup: deleting file");
    fs.unlinkSync("test.txt");
}

// Error case
try {
    const missing = fs.readFileSync("nonexistent.txt", "utf8");
} catch (err) {
    console.log(`Caught error: ${err.message}`);
} finally {
    console.log("Done with error demo");
}