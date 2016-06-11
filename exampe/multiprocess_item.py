from sys import stdin
from multiprocessing import Pool, Value
from math import factorial

import dummy


def job_fn(i):
    dummy.shared.value += factorial(i)
    print('job_fn', 'id:', i, 'value:', dummy.shared.value)


def initProcess(share):
    dummy.shared = share
    print ("initProcess")

if __name__ == '__main__':
    # allocate shared array - want lock=False in this case since we
    # aren't writing to it and want to allow multiple processes to access
    # at the same time - I think with lock=True there would be little or
    # no speedup
    toShare = Value('i', 0)

    # fork
    pool = Pool(10, initializer=initProcess, initargs=(toShare,))
    jobs = [pool.apply_async(job_fn, [i]) for i in range(10000)]
    for x in jobs:
        x.get()
    pool.close()
    pool.join()
