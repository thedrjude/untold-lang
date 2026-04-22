// Async Programming
const axios = require('axios');

console.log("=== Async Programming Demo ===");

async function main() {
    // Sequential async (slower)
    console.log("Fetching sequentially...");
    const res1 = await axios.get("https://httpbin.org/delay/1");
    console.log("First done!");

    // Parallel async (faster)
    console.log("Fetching in parallel...");
    const results = await Promise.all([
        axios.get("https://httpbin.org/get"),
        axios.get("https://httpbin.org/get"),
        axios.get("https://httpbin.org/get")
    ]);
    console.log("All done in parallel!");
}

main();

// Run functions in parallel
const task1 = () => Promise.resolve("Task 1 done");
const task2 = () => Promise.resolve("Task 2 done");

console.log("Running functions in parallel...");
Promise.all([task1(), task2()]).then(results => {
    results.forEach(r => console.log(r));
});