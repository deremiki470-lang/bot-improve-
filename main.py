import hashlib
import time
import os

def cpu_benchmark(duration_sec=10, block_size=32):
    """
    Simple CPU benchmark to simulate hashing load.
    duration_sec: how long to run test (seconds)
    block_size: bytes per hash input (affects CPU workload)
    """
    data = os.urandom(block_size)
    count = 0
    start = time.time()
    end_time = start + duration_sec

    while time.time() < end_time:
        # Simulate a hash calculation (like mining)
        data = hashlib.sha256(data).digest()
        count += 1

    elapsed = time.time() - start
    hashes_per_sec = count / elapsed

    print(f"--- CPU Benchmark Results ---")
    print(f"Duration: {elapsed:.2f} s")
    print(f"Hashes computed: {count:,}")
    print(f"Estimated speed: {hashes_per_sec:,.0f} hashes/sec")
    print(f"Equivalent: {hashes_per_sec/1e3:,.2f} kH/s, {hashes_per_sec/1e6:,.2f} MH/s")

if __name__ == "__main__":
    cpu_benchmark(duration_sec=10)
