// HTTP Requests
const axios = require('axios');

async function main() {
    // GET request
    console.log("Fetching data...");
    const res = await axios.get("https://api.github.com");
    console.log(`Status: ${res.status}`);
    console.log(`Body length: ${res.data.length}`);

    // POST request
    const postRes = await axios.post("https://httpbin.org/post", {key: "value"});
    console.log(`POST Status: ${postRes.status}`);
}

main();