from math import factorial  # noqa
import decimal as dc
import time
import argparse
import multiprocessing


SUM = 0
# p = 2000 ~ Execution time: 22.088331699371338


def calculate_current(i):  # noqa
    # print(i)
    current = dc.Decimal(pow(3 * i, 2) + 1) / dc.Decimal(factorial(3 * i))
    return current


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

    global SUM
    start = time.time()

    for i in range(iterations_count):
        SUM += calculate_current(i)

    print(SUM)
    print('Execution time: {0}'.format(time.time() - start))


if __name__ == '__main__':
    main()
