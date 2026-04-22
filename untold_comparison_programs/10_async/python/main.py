# Async Programming
import asyncio
import aiohttp

print("=== Async Programming Demo ===")

async def fetch_data(session, url):
    async with session.get(url) as response:
        return await response.text()

async def main():
    # Sequential async (slower)
    print("Fetching sequentially...")
    async with aiohttp.ClientSession() as session:
        res1 = await fetch_data(session, "https://httpbin.org/delay/1")
        print("First done!")

        # Parallel async (faster)
        print("Fetching in parallel...")
        tasks = [
            fetch_data(session, "https://httpbin.org/get"),
            fetch_data(session, "https://httpbin.org/get"),
            fetch_data(session, "https://httpbin.org/get")
        ]
        results = await asyncio.gather(*tasks)
        print("All done in parallel!")

asyncio.run(main())

# Run functions in parallel
import concurrent.futures

def task1():
    return "Task 1 done"

def task2():
    return "Task 2 done"

print("Running functions in parallel...")
with concurrent.futures.ThreadPoolExecutor() as executor:
    futures = [executor.submit(task1), executor.submit(task2)]
    for f in concurrent.futures.as_completed(futures):
        print(f.result())