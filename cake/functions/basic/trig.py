# Trigonometric functions
from cake.core.types.integer import Integer
from ..base import MaskFunctionTemp
import math

__all__ = (
    "Sin", "Cos", "Tan",
    "ASin", "ACos", "ATan",
    "SinH", "CosH", "TanH",
    "Sec", "Cosec", "Cot"
)


# SIN COS TAN

class Sin(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "sin", math.sin, type=type)

class Cos(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "cos", math.cos, type=type)

class Tan(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "tan", math.tan, type=type)

# INVERSE TRIG FUNCS

class ASin(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "asin", math.asin, type=type)

class ACos(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "acos", math.asin, type=type)

class ATan(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "atan", math.atan, type=type)

# HYPERBOLIC TRIG FUNCTIONS
class SinH(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "asin", math.sinh, type=type)

class CosH(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "acos", math.cosh, type=type)

class TanH(MaskFunctionTemp):
    def __init__(self, value, *, type: str = "radians") -> None:
        super().__init__(value, "atan", math.tanh, type=type)

# SEC COT COSEC

def Sec(value, *, type: str = "radians"):
    x = Cos(value, type=type)
    x.execAfter(lambda x: Integer(1) / x)
    return x

def Cosec(value, *, type: str = "radians"):
    x = Sin(value, type=type)
    x.execAfter(lambda x: Integer(1) / x)
    return x

def Cot(value, *, type: str = "radians"):
    x = Tan(value, type=type)
    x.execAfter(lambda x: Integer(1) / x)
    return x
