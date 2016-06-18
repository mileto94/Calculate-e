from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing
# from ctypes import *  # noqa

import tmp_dummy


# p = 2000 ~ Execution time: 22.088331699371338
PROCESSES_COUNT = 0
IS_QUIET = False
# dc.getcontext().prec = 999999999
final_res = dc.Decimal(0)
PREC_COUNT = 2000


def calculate_current(i):  # noqa
    current = dc.Decimal((pow(3 * i, 2) + 1)) / dc.Decimal(factorial(3 * i))
    if not IS_QUIET:
        # print('calculate_current', 'id:', i, 'value:', tmp_dummy.final_sum.value)
        print('process {} is calculating calculate_current with index {}'.format(multiprocessing.current_process(), i))
    return current

def add_current(current):  # noqa
    global final_res
    dc.getcontext().prec = PREC_COUNT
    final_res += current
    print('Final result: {}'.format(final_res))
    tmp_dummy.final_sum += current
    # print(current)


def init_process(share):  # noqa
    global PROCESSES_COUNT
    PROCESSES_COUNT += 1
    tmp_dummy.final_sum = share
    if not IS_QUIET:
        print('Init Process {}'.format(multiprocessing.current_process().name))


def main():  # noqa
    global IS_QUIET, PREC_COUNT, final_res
    parser = argparse.ArgumentParser(description='''
This is multiprocessing program which calculates e as a finite sum.
e=∑((3k)^2 + 1) / ((3k)!), k =0,... ,∞''')
    parser.add_argument(
        '-q',
        action='store_true',
        default=False,
        help='Specify quiet mode of calculating. Quiet mode does not print output during calculations. By default it is disabled.')  # noqa

    parser.add_argument(
        '-p',
        metavar='iterations_count',
        type=int,
        default=2000,
        help='Specify number of iterations (items in sequence). If not specified it is set to 2 000.')  # noqa

    parser.add_argument(
        '-t',
        metavar='cores_count',
        type=int,
        default=multiprocessing.cpu_count(),
        help='Specify number of cores to be used for the calculation. If not specified it is set to max cpu count of current PC.')  # noqa

    parser.add_argument(
        '-d',
        metavar='digits_precision',
        type=int,
        default=20000,
        help='Specify set precision for calculation. If not specified it is set to 20 000.')  # noqa

    parser.add_argument(
        '-o',
        metavar='filename',
        type=str,
        default='result.txt',
        help='Specify name of file with calcuated result. Default value is "result.txt".')  # noqa

    args = parser.parse_args()

    iterations_count = args.p
    processors_number = args.t
    digits_precision = args.d
    IS_QUIET = args.q
    filename = args.o

    PREC_COUNT = digits_precision
    dc.getcontext().prec = digits_precision
    final_res = dc.Decimal(0)

    # allocate shared array - want lock=False in this case since we
    # aren't writing to it and want to allow multiple processes to access
    # at the same time - I think with lock=True there would be little or
    # no speedup
    result = multiprocessing.Value('f', 0.)
    # result = multiprocessing.Value(c_longdouble, 0.)

    # fork
    pool = multiprocessing.Pool(
        processors_number, initializer=init_process, initargs=(result,))

    start = time.time()

    jobs = [pool.apply_async(calculate_current, [i], callback=add_current) for i in range(iterations_count)]  # noqa

    for x in jobs:
        x.get()
    end = time.time()

    if not IS_QUIET:
        print('Number of started processes: {count}'.format(count=pool._processes))  # noqa
        print('RESULT: {}'.format(final_res))

    # print(tmp_dummy.final_sum)
    print(tmp_dummy.final_sum == final_res)
    print('Total execution time: {time_took}'.format(time_took=(end - start)))  # noqa

    with open(filename, 'w') as opened_file:
        opened_file.write(str(final_res))

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
