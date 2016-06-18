from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing
from ctypes import *  # noqa

import dummy
# dummy.final_sum = dc.Decimal(dummy.final_sum)

# p = 2000 ~ Execution time: 22.088331699371338
PROCESSES_COUNT = 0
IS_QUIET = False

def calculate_current(i):  # noqa
    # print(i)
    a = (pow(3 * i, 2) + 1)
    b = (factorial(3 * i))
    # print(a.value)
    # print(b.value)
    # current = c_ulonglong(pow(3 * i, 2) + 1).value / c_ulonglong(factorial(3 * i)).value  # noqa
    current = dc.Decimal(a / b)
    print('current', current)
    dummy.final_sum.value += current
    if not IS_QUIET:
        print('calculate_current', 'id:', i, 'value:', dummy.final_sum.value)


# def job_fn(i):  # noqa
#     dummy.final_sum.value += factorial(i)
#     print('job_fn', 'id:', i, 'value:', dummy.final_sum.value)


def init_process(share):  # noqa
    global PROCESSES_COUNT
    PROCESSES_COUNT += 1
    dummy.final_sum = share
    if not IS_QUIET:
        print('Init Process N {}'.format(PROCESSES_COUNT))


def main():  # noqa
    global PROCESSES_COUNT, IS_QUIET
    parser = argparse.ArgumentParser(description='Calculate e.')
    # parser.add_argument(
    #     'integers', metavar='N', type=int, nargs='+',
    #     help='an integer for the accumulator')
    parser.add_argument(
        '-q',
        # dest='accumulate',
        action='store_true',
        default=False,
        help='Specify quiet mode of calculating. Quiet mode does not print output during calculations. By default it is disabled.')  # noqa

    parser.add_argument(
        '-p',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        default=2000,
        help='Specify number of iterations (items in sequence). If not specified it is set to 2 000.')  # noqa

    parser.add_argument(
        '-t',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        default=multiprocessing.cpu_count(),
        help='Specify number of processors to be used for the calculation. If not specified it is set to max cpu count of current PC.')  # noqa

    parser.add_argument(
        '-d',
        # dest='accumulate', action='store_const',
        metavar='N',
        type=int,
        default=20000,
        help='Specify set precision for calculation. If not specified it is set to 20 000.')  # noqa

    args = parser.parse_args()
    # iterations_count = args.p if args.p else 2000
    # processors_number = args.t if args.t else multiprocessing.cpu_count()
    # digits_precision = args.d if args.t else 20000
    # IS_QUIET = True if args.q else False

    iterations_count = args.p
    processors_number = args.t
    digits_precision = args.d
    IS_QUIET = args.q
    # print('iterations_count', iterations_count)
    # print('processors_number', processors_number)
    # print('digits_precision', digits_precision)
    # print('IS_QUIET', IS_QUIET)
    # return
    dc.getcontext().prec = digits_precision

    # for i in range(iterations_count):
    #     SUM += calculate_current(i)

    # allocate shared array - want lock=False in this case since we
    # aren't writing to it and want to allow multiple processes to access
    # at the same time - I think with lock=True there would be little or
    # no speedup
    result = multiprocessing.Value('d', 0.)
    # result = multiprocessing.Value(c_longdouble, 0.)

    # fork
    pool = multiprocessing.Pool(
        processors_number, initializer=init_process, initargs=(result,))

    start = time.time()

    jobs = [pool.apply_async(calculate_current, [i]) for i in range(iterations_count)]  # noqa

    for x in jobs:
        x.get()

    if not IS_QUIET:
        print('Number of started processes: {count}'.format(count=PROCESSES_COUNT))  # noqa

    print(result.value)
    print('Total execution time: {time_took}'.format(time_took=(time.time() - start)))  # noqa

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
