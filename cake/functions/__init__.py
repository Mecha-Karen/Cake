from .base import *
from .prime import *
from .basic import *

def factors(n):
    result = reduce(
        list.__add__, ([i, n // i] for i in range(1, int(n ** 0.5) + 1) if n % i == 0)
    )
    factors_ = set(result)

    return sorted(factors_)
