from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing


# p = 2000 ~ Execution time: 22.088331699371338

PROCESSES_COUNT = 0
IS_QUIET = False
final_res = dc.Decimal(0)


def calculate_current(i):  # noqa
    current = dc.Decimal((pow(3 * i, 2) + 1)) / dc.Decimal(factorial(3 * i))
    if not IS_QUIET:
        print('current: {}'.format(current))
        print('process {} is calculating calculate_current with index {}'.format(multiprocessing.current_process(), i))  # noqa
    return current


def add_current(current):  # noqa
    global final_res
    final_res += current
    print('Final result: {}'.format(final_res))


def init_process():  # noqa
    global PROCESSES_COUNT
    PROCESSES_COUNT += 1
    if not IS_QUIET:
        print('Init Process {}'.format(multiprocessing.current_process().name))


def main():  # noqa
    global IS_QUIET, final_res

    parser = argparse.ArgumentParser(description='Calculate e.')
    parser.add_argument(
        '-q',
        action='store_true',
        default=False,
        help='Specify quiet mode of calculating. Quiet mode does not print output during calculations. By default it is disabled.')  # noqa

    parser.add_argument(
        '-p',
        metavar='N',
        type=int,
        default=2000,
        help='Specify number of iterations (items in sequence). If not specified it is set to 2 000.')  # noqa

    parser.add_argument(
        '-t',
        metavar='N',
        type=int,
        default=multiprocessing.cpu_count(),
        help='Specify number of processors to be used for the calculation. If not specified it is set to max cpu count of current PC.')  # noqa

    parser.add_argument(
        '-d',
        metavar='N',
        type=int,
        default=20000,
        help='Specify set precision for calculation. If not specified it is set to 20 000.')  # noqa

    args = parser.parse_args()

    iterations_count = args.p
    processors_number = args.t
    digits_precision = args.d
    IS_QUIET = args.q

    dc.getcontext().prec = digits_precision
    final_res = dc.Decimal(0)

    # fork
    pool = multiprocessing.Pool(processors_number, initializer=init_process)
    start = time.time()

    jobs = [pool.apply_async(calculate_current, [i], callback=add_current) for i in range(iterations_count)]  # noqa

    for x in jobs:
        x.get()

    if not IS_QUIET:
        print('Number of started processes: {count}'.format(count=PROCESSES_COUNT))  # noqa

    print('Total execution time: {time_took}'.format(time_took=(time.time() - start)))  # noqa

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
