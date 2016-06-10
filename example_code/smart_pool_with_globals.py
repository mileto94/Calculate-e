# creates 4 processes with NEGATIVE diff between items of e

import time
import argparse

from multiprocessing import Pool, Array
from math import factorial

import decimal as dc
# set the precision
dc.getcontext().prec = 2000


def calculate_e(k):
    print('k', k)
    print('shared_data', shared_data)
    return dc.Decimal((pow(3 * k, 2) + 1)) / dc.Decimal(factorial(3 * k))  # noqa

latest_value = 0
result = 0
lower_border = dc.Decimal(pow(10, -1000))


def start_new_process(shared):
    print('start')
    shared_data = shared


def calculation_callback(current):
    print('shared_data', shared_data)
    diff = current - latest_value
    print('diff', diff)
    print('lower_border', lower_border)

    if diff < lower_border:
        print('EXIT')
        quit()
    result += current
    print('latest_value', latest_value)
    latest_value = current


# num_samples_in_total=10000
def run(num_samples_in_total=100, num_parallel_blocks=4):
    shared = Array('c', 20, lock=False)

    pool = Pool(processes=num_parallel_blocks, initializer=start_new_process, initargs=[shared])

    # num_samples_per_worker = num_samples_in_total / num_parallel_blocks
    # print("Making {} samples per worker".format(num_samples_per_worker))
    # nbr_trials_per_process = [num_samples_per_worker] * num_parallel_blocks
    # partial_sums = pool.map(calculate_e, nbr_trials_per_process)

    t1 = time.time()
    # partial_sums = [pool.apply_async(calculate_e, i, b_print) for i in range(num_samples_in_total)]
    for i in range(num_samples_in_total):
        current_results = pool.apply_async(calculate_e, [i], {}, calculation_callback)
        current_results.get()

    # e_estimate = sum(partial_sums)
    # print(partial_sums)

    # print("Estimated e", e_estimate)
    print('result', result)
    print("Delta:", time.time() - t1)


def main():
    # parser = argparse.ArgumentParser(description='Process some integers.')
    # parser.add_argument(
    #     'integers', metavar='N', type=int, nargs='+',
    #     help='an integer for the accumulator')
    # parser.add_argument(
    #     '--sum', dest='accumulate', action='store_const',
    #     const=sum, default=max,
    #     help='sum the integers (default: find the max)')

    # args = parser.parse_args()
    # print(args)
    run()

if __name__ == '__main__':
    main()
