# HTTP Requests
import requests

# GET request
print("Fetching data...")
res = requests.get("https://api.github.com")
print(f"Status: {res.status_code}")
print(f"Body length: {len(res.text)}")

# POST request
post_res = requests.post("https://httpbin.org/post", json={"key": "value"})
print(f"POST Status: {post_res.status_code}")