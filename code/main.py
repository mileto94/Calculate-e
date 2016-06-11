from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing
import numpy as np
from ctypes import c_longdouble

import dummy
# dummy.final_sum = dc.Decimal(dummy.final_sum)

# p = 2000 ~ Execution time: 22.088331699371338


def calculate_current(i):  # noqa
    print(i)
    current = dc.Decimal(pow(3 * i, 2) + 1) / dc.Decimal(factorial(3 * i))
    print('current', current)
    dummy.final_sum.value += current
    print('calculate_current', 'id:', i, 'value:', dummy.final_sum.value)


# def job_fn(i):  # noqa
#     dummy.final_sum.value += factorial(i)
#     print('job_fn', 'id:', i, 'value:', dummy.final_sum.value)


def init_process(share):  # noqa
    dummy.final_sum = share
    print ("initProcess")


def main():  # noqa

    parser = argparse.ArgumentParser(description='Calculate e.')
    # parser.add_argument(
    #     'integers', metavar='N', type=int, nargs='+',
    #     help='an integer for the accumulator')
    parser.add_argument(
        '-q',
        # dest='accumulate', action='store_const',
        help='Specify quit mode of calculating.')

    parser.add_argument(
        '-p',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        help='Specify number of iterations (items in sequence).')

    parser.add_argument(
        '-t',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        help='Specify number of processors to be used for the calculation.')

    parser.add_argument(
        '-d',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        help='Specify set precision for calculation.')

    args = parser.parse_args()
    iterations_count = args.p if args.p else 2000
    processors_number = args.t if args.t else multiprocessing.cpu_count()
    digits_precision = args.t if args.t else 20000
    dc.getcontext().prec = digits_precision

    # for i in range(iterations_count):
    #     SUM += calculate_current(i)

    # allocate shared array - want lock=False in this case since we
    # aren't writing to it and want to allow multiple processes to access
    # at the same time - I think with lock=True there would be little or
    # no speedup
    result = multiprocessing.Value('f', 0.)

    # fork
    pool = multiprocessing.Pool(processors_number, initializer=init_process, initargs=(result,))

    start = time.time()

    jobs = [pool.apply_async(calculate_current, [i]) for i in range(iterations_count)]

    for x in jobs:
        x.get()

    print(result.value)
    print('Execution time: {0}'.format(time.time() - start))

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
