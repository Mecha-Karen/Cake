from ..base import MaskFunctionTemp
import math
from collections.abc import Iterable

__all__ = (
    "Sqrt", "Abs",
    "Ceil", "Comb", "CopySign",
    "Dist",
    "Erf", "Erfc", "Exp", "ExpM1",
    "Factorial", "Floor", "FMod", "FRExp", "FSum",
    "Gamma", "GCD",
    "Hypot",
    "ISqrt",
    "LCM", "LDExp", "LGamma", "Log", "Log10", "Log1p", "Log2",
    "ModF",
    "NextAfter",
    "Perm", "Pow",
    "Remainder",
    "Trunc",
    "ULP"
)


class Sqrt(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "") -> None:
        super().__init__(value, "sqrt", math.sqrt, type=type)


class Abs(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "abs", math.fabs, type=type)


class Ceil(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "") -> None:
        super().__init__(value, "ceil", math.ceil, type=type)


class Comb(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "comb", math.comb, type=type)


class CopySign(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "copysign", math.copysign, type=type)


class Dist(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "dist", math.dist, type=type)


class Erf(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "erf", math.erf, type=type)


class Erfc(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "erfc", math.erfc, type=type)


class Exp(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "exp", math.exp, type=type)


class ExpM1(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "expm1", math.expm1, type=type)


class Erf(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "erf", math.erf, type=type)


class Factorial(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "factorial", math.factorial, type=type)


class Floor(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "floor", math.floor, type=type)


class FMod(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "fmod", math.fmod, type=type)


class FRExp(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "frexp", math.frexp, type=type)


class FSum(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "fsum", math.fsum, type=type)


class Gamma(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "gamma", math.gamma, type=type)


class GCD(MaskFunctionTemp):
    def __init__(self, *x, type: str = "") -> None:
        if len(x) == 1 and isinstance(x[0], Iterable):
            x = x[0]

        super().__init__(x, "gcd", math.gcd, type=type)


class Hypot(MaskFunctionTemp):
    def __init__(self, *x, type: str = "") -> None:
        if len(x) == 1 and isinstance(x[0], Iterable):
            x = x[0]

        super().__init__(x, "hypot", math.hypot, type=type)


class ISqrt(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "isqrt", math.isqrt, type=type)


class LCM(MaskFunctionTemp):
    def __init__(self, *x, type: str = "") -> None:
        if len(x) == 1 and isinstance(x[0], Iterable):
            x = x[0]

        super().__init__(x, "lcm", math.lcm, type=type)


class LDExp(MaskFunctionTemp):
    def __init__(self, x, i, *, type: str = "") -> None:
        super().__init__((x, i), "ledexp", math.ldexp, type=type)


class LGamma(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "lgamma", math.lgamma, type=type)


class Log(MaskFunctionTemp):
    def __init__(self, x, base = None, *, type: str = "") -> None:
        super().__init__((x, base), "log", math.log, type=type)


class Log10(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "log10", math.log10, type=type)


class Log1p(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "log1p", math.log1p, type=type)


class Log2(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "log2", math.log2, type=type)


class ModF(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "modf", math.modf, type=type)


class NextAfter(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "nextafter", math.nextafter, type=type)


class Perm(MaskFunctionTemp):
    def __init__(self, n, k, *, type: str = "") -> None:
        super().__init__((n, k), "perm", math.perm, type=type)


class Pow(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "pow", math.pow, type=type)


class Remainder(MaskFunctionTemp):
    def __init__(self, x, y, *, type: str = "") -> None:
        super().__init__((x, y), "Remainder", math.remainder, type=type)


class Trunc(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "trunc", math.trunc, type=type)


class ULP(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "ulp", math.ulp, type=type)
