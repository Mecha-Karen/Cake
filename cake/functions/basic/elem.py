from ..base import MaskFunctionTemp
import math

__all__ = (
    "Sqrt", "Abs",
    "Ceil", "Comb", "CopySign",
    "Dist",
    "Erf", "Erfc", "Exp", "ExpM1",
    "Factorial", "Floor",
)


class Sqrt(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "") -> None:
        super().__init__(value, "sqrt", math.sqrt, type=type)


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


class Abs(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "fabs", math.fabs, type=type)


class Factorial(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "factorial", math.factorial, type=type)


class Floor(MaskFunctionTemp):
    def __init__(self, x, *, type: str = "") -> None:
        super().__init__(x, "floor", math.floor, type=type)
