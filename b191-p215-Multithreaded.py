#!/bin/env python3.6

# proof-of-work-example.py
# now multi-threaded!

import hashlib
import time
import threading

max_nonce = (2 ** 31) - 1
THREADS = 1


# multi-thread memory space
# each thread has its own entry in the array
class Result:
    res = []

    def __init__(self):
        for t in range(THREADS):
            self.res.append(0)


def worker(header, nonce, target, thread_nr, memory_pool):
    hash_result = hashlib.sha256(str(str(header)+str(nonce)).encode("UTF-8")).hexdigest()

    if int(hash_result, 16) < target:
        print("Sucsess with nonce %d" % nonce)
        print("Hash is %s" % hash_result)
        memory_pool.res[thread_nr] = nonce
        return
    memory_pool.res[thread_nr] = -1


def proof_of_work(header, difficulty_bits, result):
    target = 2 ** (256-difficulty_bits)

    for nonce in range(0, max_nonce, THREADS):
        threads = []
        for i in range(THREADS):
            t = threading.Thread(target=worker, name="worker" + str(i + 1), args=(header, nonce + i, target, i, result))
            threads.append(t)
            t.start()

        success = False
        success_thread = -1
        for i in range(THREADS):
            threads[i].join()
            if result.res[i] is not -1:
                success = True
                success_thread = i

        if success:
            return nonce + success_thread


    print("Failed after %d (max_nonce) tries" % nonce)
    return nonce


if __name__ == "__main__":
    nonce       = 0
    hash_result = ""
    result = Result()

    for difficulty_bits in range(32):
        difficulty = 2 ** difficulty_bits
        print("Difficulty: %ld (%d bits)" % (difficulty, difficulty_bits))

        print("Starting search...")

        start_time = time.time()

        new_block = "test block with transactions" + hash_result

        nonce = proof_of_work(new_block, difficulty_bits, result)
        hash_result = str(nonce)

        end_time = time.time()

        elapsed_time = end_time - start_time
        print("Elapsed time: %.4f seconds" % elapsed_time)

        if elapsed_time > 0:
            hash_power = float(int(nonce)/elapsed_time)
            print("Hashing Power: %ld hashes per second" % hash_power)

        print("")
