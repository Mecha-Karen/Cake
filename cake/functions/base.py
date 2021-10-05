# Base matmatical functions re-written to handle unknowns and other functions
from functools import reduce


def factors(n):
    result = reduce(list.__add__, ([i, n//i] for i in range(1, int(n**0.5) + 1) if n % i == 0))
    factors_ = set(result)
    
    return sorted(factors_)
