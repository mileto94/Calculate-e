from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing

# p = 2000 ~ Execution time: 22.088331699371338

DIGITS_PREC = pow(2, 20)
dc.getcontext().prec = DIGITS_PREC

IS_QUIET = False
final_res = dc.Decimal(0)


def calculate_current(i):  # noqa
    current = dc.Decimal((pow(3 * i, 2) + 1) / factorial(3 * i))
    if not IS_QUIET:
        print('current: {}'.format(current))
        print('process {} is calculating calculate_current with index {}'.format(multiprocessing.current_process(), i))  # noqa
    return current


def add_current(current):  # noqa
    global final_res
    dc.getcontext().prec = DIGITS_PREC
    final_res += current
    print(current)
    print('Final result: {}'.format(final_res))


def init_process():  # noqa
    if not IS_QUIET:
        print('Init Process {}'.format(multiprocessing.current_process().name))


def main():  # noqa
    """
    Create pool of Processes. Each process receives number of item in the sum
and uses it in calculate_current function.
    """
    global IS_QUIET, final_res, DIGITS_PREC

    parser = argparse.ArgumentParser(description='''
This is multiprocessing program which calculates e as a finite sum with Python:
e=∑((3k)^2 + 1) / ((3k)!), where k = 0,... ,∞''')
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
    cores_number = args.t
    digits_precision = args.d
    IS_QUIET = args.q
    filename = args.o

    DIGITS_PREC = digits_precision
    dc.getcontext().prec = digits_precision

    # fork
    pool = multiprocessing.Pool(cores_number, initializer=init_process)
    start = time.time()

    jobs = [pool.apply_async(calculate_current, [i], callback=add_current) for i in range(iterations_count)]  # noqa

    for x in jobs:
        x.get()

    if not IS_QUIET:
        print('Number of started processes: {count}'.format(count=pool._processes))  # noqa
        print('RESULT: {}'.format(final_res))

    print('Total execution time: {time_took}'.format(time_took=(time.time() - start)))  # noqa

    with open(filename, 'w') as opened_file:
        opened_file.write(str(final_res))

    pool.close()
    pool.join()


if __name__ == '__main__':
    main()
