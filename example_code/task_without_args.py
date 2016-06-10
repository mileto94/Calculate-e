from multiprocessing import Pool

from math import factorial
import time

import decimal as dc
# set the precision
dc.getcontext().prec = 2000


def calculate_e(k):
    print('k', k)
    SUM = dc.Decimal(0)
    lower_border = dc.Decimal(pow(10, -1000))

    print('\nlower_border', lower_border)
    print()

    k = int(k)
    latest_value = 0
    for index in range(k):
        current = dc.Decimal((pow(3 * index, 2) + 1)) / dc.Decimal(factorial(3 * index))  # noqa
        diff = current - latest_value

        print('iteration N: ', index)
        # print('difference', diff)

        if diff < lower_border:
            break
        SUM += current
        # latest_value = current

        # print('SUM', SUM)
        # print()

    return SUM


def run():
    num_samples_in_total = 10000
    num_parallel_blocks = 1

    pool = Pool(processes=num_parallel_blocks)

    num_samples_per_worker = num_samples_in_total / num_parallel_blocks
    print("Making {} samples per worker".format(num_samples_per_worker))
    nbr_trials_per_process = [num_samples_per_worker] * num_parallel_blocks

    t1 = time.time()
    partial_sums = pool.map(calculate_e, nbr_trials_per_process)
    e_estimate = sum(partial_sums)

    print("Estimated e", e_estimate)
    print("Delta:", time.time() - t1)


def main():
    run()

if __name__ == '__main__':
    main()
