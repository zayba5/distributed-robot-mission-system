import requests
import concurrent.futures
import time
import statistics

URL = "http://localhost:5000/missions"

TOTAL_REQUESTS = 100
CONCURRENT_USERS = 20


def submit_mission(number):

    start = time.time()

    try:
        response = requests.post(
            URL,
            json={
                "start_x": 0,
                "start_y": 0,
                "destination_x": number % 10,
                "destination_y": number % 10,
                "priority": 1
            },
            timeout=10
        )

        elapsed = (
            time.time() - start
        ) * 1000

        return (
            response.status_code,
            elapsed
        )

    except Exception:
        elapsed = (
            time.time() - start
        ) * 1000

        return (0, elapsed)


print("Starting load test...")
print(
    f"Requests: {TOTAL_REQUESTS}, "
    f"Concurrency: {CONCURRENT_USERS}"
)

start_test = time.time()

with concurrent.futures.ThreadPoolExecutor(
    max_workers=CONCURRENT_USERS
) as executor:

    results = list(
        executor.map(
            submit_mission,
            range(TOTAL_REQUESTS)
        )
    )

total_time = time.time() - start_test

successful = [
    latency
    for status, latency in results
    if status == 201
]

failed = TOTAL_REQUESTS - len(successful)

print("\n===== RESULTS =====")

print(f"Successful: {len(successful)}")
print(f"Failed: {failed}")

if successful:

    print(
        f"Average latency: "
        f"{statistics.mean(successful):.2f} ms"
    )

    sorted_times = sorted(successful)

    p95_index = int(
        0.95 * len(sorted_times)
    ) - 1

    print(
        f"P95 latency: "
        f"{sorted_times[p95_index]:.2f} ms"
    )

print(
    f"Total test time: "
    f"{total_time:.2f} seconds"
)
