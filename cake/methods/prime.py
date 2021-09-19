"""
MIT License

Copyright (c) 2021 Mecha Karen

Permission is hereby granted, free of charge, to any person obtaining a copy
of this software and associated documentation files (the "Software"), to deal
in the Software without restriction, including without limitation the rights
to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
copies of the Software, and to permit persons to whom the Software is
furnished to do so, subject to the following conditions:

The above copyright notice and this permission notice shall be included in all
copies or substantial portions of the Software.

THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
SOFTWARE.

Generate factor tree of a integer
"""
from cake.abc import ODD_NUMBERS


def _is_even(num):
    return bool(num % 2 == 0)


def _is_odd(num):
    return _is_even(num) != True


def is_prime(n: int) -> bool:
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


def factor_tree(x: int) -> list:
    if is_prime(x):
        return [x]

    tree = []

    if _is_even(x):
        current = x
        while not is_prime(current) and _is_even(current):
            current = current / 2
            tree.append(2)

        
        if is_prime(current):
            tree.append(current)
            return tree


        x = current


    if _is_odd(x):

        while not is_prime(x):
            groups = list(filter(lambda _: x % _ == 0 and _ != x, ODD_NUMBERS))


            if not groups:
                tree.append(x)
                break

            biggest = groups[-1]

            if not is_prime(biggest):
                as_tree = factor_tree(biggest)

                tree.extend(as_tree)
            else:
                tree.append(biggest)

            x = x / biggest

        tree.append(x)

    # Break tree down further
    to_break = filter(lambda sub: not is_prime(sub), tree)
    for factor in to_break:
        factorTree = factor_tree(factor)

        tree.remove(factor)
        tree.extend(factorTree)
    
    return tree
