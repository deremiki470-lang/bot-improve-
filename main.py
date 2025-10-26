import time
import multiprocessing as mp
import numpy as np

PROG_LEN = 512        # instructions per program
TEST_ITERS = 100_000  # programs per process (tune this for speed/accuracy)

# Fast xorshift64 PRNG
def xorshift64(state):
    x = state[0]
    x ^= (x << 13) & 0xFFFFFFFFFFFFFFFF
    x ^= (x >> 7) & 0xFFFFFFFFFFFFFFFF
    x ^= (x << 17) & 0xFFFFFFFFFFFFFFFF
    state[0] = x & 0xFFFFFFFFFFFFFFFF
    return state[0]

def gen_program(state):
    opcodes = np.empty(PROG_LEN, dtype=np.uint8)
    operands = np.empty(PROG_LEN, dtype=np.uint64)
    for i in range(PROG_LEN):
        r = xorshift64(state)
        opcodes[i]  = r & 0xFF
        operands[i] = (r >> 8) & 0xFFFFFFFFFFFF
    return opcodes, operands

def worker(seed):
    state = [seed ^ 0x123456789ABCDEF0]
    t0 = time.perf_counter()
    for _ in range(TEST_ITERS):
        gen_program(state)
    t1 = time.perf_counter()
    return TEST_ITERS / (t1 - t0)

def main():
    cores = mp.cpu_count()
    print(f"Detected {cores} logical cores — launching benchmark...")
    with mp.Pool(cores) as pool:
        results = pool.map(worker, [i * 0xABCDEF for i in range(cores)])

    total = sum(results)
    per_core = [round(r, 1) for r in results]
    print(f"\nPer-core programs/sec: {per_core}")
    print(f"Total: {total:,.2f} programs/sec across {cores} cores")

if __name__ == "__main__":
    main()
