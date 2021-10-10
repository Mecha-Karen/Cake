from cake.abc import ODD_NUMBERS, IntegerType
from math import sqrt


def _is_even(num: IntegerType) -> bool:
    return bool(num % 2 == 0)


def _is_odd(num: IntegerType) -> bool:
    return _is_even(num) != True


def is_prime(n: IntegerType) -> bool:
    if n <= 3:
        return n > 1
    if n % 2 == 0 or n % 3 == 0:
        return False
    i = 5
    while i ** 2 <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6
    return True


def is_coprime(x: IntegerType, y: IntegerType) -> bool:
    while y != 0:
        x, y = y, x % y
    return x == 1


def factor_tree(x: IntegerType) -> list:
    if hasattr(x, "value"):
        x = int(x.value)

    if is_prime(x):
        return [x]
    tree = list()

    while _is_even(x) and not is_prime(x):
        # Constantly divide by 2, till odd or is prime
        x /= 2
        tree.append(2)

    while _is_odd(x) and not is_prime(x):
        is_square = sqrt(x)
        if int(is_square) - is_square == 0:
            x /= is_square
            tree.append(is_square)
            break

        groups = list(filter(lambda _: x % _ == 0, ODD_NUMBERS))
        if groups:
            biggest = groups[-1]
            if not is_prime(biggest):
                subTree = factor_tree(biggest)
                tree.extend(subTree)
                x /= biggest

    tree.append(x)

    invalidFactors = list(filter(lambda _: not is_prime(_), tree))
    if invalidFactors:
        for toFactorise in invalidFactors:
            tree.remove(toFactorise)
            tree.extend(factor_tree(toFactorise))

    return tree
