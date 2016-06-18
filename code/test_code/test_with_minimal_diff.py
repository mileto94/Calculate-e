from math import factorial  # noqa
import decimal as dc
import time

dc.getcontext().prec = 2000

SUM = 0
k = 100000
lower_border = dc.Decimal(pow(10, -100))


def calculate_current(i):  # noqa
    print(i)
    current = dc.Decimal(pow(3 * i, 2) + 1) / dc.Decimal(factorial(3 * i))
    return current


def main():  # noqa
    global SUM
    latest_value = 0
    start = time.time()
    for i in range(k):
        current = calculate_current(i)
        if current - latest_value < lower_border:
            break
        SUM += current
    print(SUM)
    print('Execution time: {0}'.format(time.time() - start))


if __name__ == '__main__':
    main()
