import typing
import cake


class Fraction(object):
    def __init__(self, numerator: typing.Any, denominator: typing.Any) -> None:
        self.numerator = numerator
        self.denominator = denominator

    def __repr__(self) -> str:
        return f'Fraction(numerator={self.numerator} denominator={self.denominator})'
