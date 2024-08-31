import asyncio
import aiohttp
import time

# Number of requests per second
requests_per_second = 100

# Total duration in seconds
duration = 10

# Calculate total requests
total_requests = requests_per_second * duration

# Success and failure counters
success_count = 0
fail_count = 0

# URL to send requests
url = 'http://localhost'

async def fetch(session):
    global success_count, fail_count
    try:
        async with session.get(url) as response:
            status_code = response.status
            if status_code == 200:
                success_count += 1
            else:
                fail_count += 1
            proxy_jump = response.headers.get('X-Proxy-Jump', 'None')
            print(f"Status Code = {status_code}, Proxy Jump = {proxy_jump}")
    except aiohttp.ClientError as e:
        fail_count += 1
        print(f"Request failed: {e}")

async def run_requests():
    # Create a session
    async with aiohttp.ClientSession() as session:
        tasks = []
        for _ in range(total_requests):
            task = asyncio.ensure_future(fetch(session))
            tasks.append(task)
            if len(tasks) >= requests_per_second:
                # Wait for tasks to complete every second
                await asyncio.gather(*tasks)
                tasks = []
                await asyncio.sleep(1)

async def main():
    start_time = time.time()
    await run_requests()
    end_time = time.time()
    print(f"Total Requests: {total_requests}")
    print(f"Successful Requests (Status 200): {success_count}")
    print(f"Failed Requests: {fail_count}")
    print(f"Duration: {end_time - start_time} seconds")

# Run the main function
if __name__ == '__main__':
    asyncio.run(main())
