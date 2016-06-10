from math import factorial
import decimal as dc
# set the precision
dc.getcontext().prec = 2000


def calculate(k):
    SUM = dc.Decimal(0)
    lower_border = dc.Decimal(pow(10, -10000))

    print('\nlower_border', lower_border)
    print()

    latest_value = 0
    for index in range(k):
        current = dc.Decimal((pow(3 * index, 2) + 1)) / dc.Decimal(factorial(3 * index))
        diff = current - latest_value

        print('iteration N: ', index)
        print('difference', diff)

        if diff < lower_border:
            break
        SUM += current
        latest_value = current

        # print('SUM', SUM)
        print()

    print(SUM)


calculate(100000)
