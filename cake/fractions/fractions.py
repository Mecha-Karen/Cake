from __future__ import annotations

import typing
import cake

class Fraction(object):
    """
    A fraction in mathmatical terms is simply `x / y`. However, this class should only be used if X and Y should not be evaluated.
    Either for powers, or maintaing an accurate answer

    Parameters
    ----------
    numerator: :class:`~typing.Any`
        The numerator for the fraction, also known as the top number
    denominator: :class:`~typing.Any`
        The denominator for the fraction, also known as the bottom number
    co: :class:`~typing.Any`
        The coefficient for the fraction, used for representing mixed fractions.
    """
    def __init__(self, numerator: typing.Any, denominator: typing.Any, *, co: typing.Any = None) -> None:
        self.numerator = numerator
        self.denominator = denominator
        self.co = co

    def flip(self) -> Fraction:
        """ Flips the denominator and numerator """
        return Fraction(self.denominator, self.numerator, co=self.co)

    def topHeavy(self) -> Fraction:
        """ Returns an improper fraction, based on the current fraction """
        return Fraction((self.numerator * self.co), self.denominator)

    def add(self, O: Fraction) -> Fraction:
        """ Returns N + O, O's detominator must be equal to N's """
        if not isinstance(O, Fraction):
            O = Fraction(numerator=O, denominator=1)

        if O.denominator != self.denominator:
            raise ValueError(f'Denominators must the same, expected {self.denominator} got {O.denominator}')

        res = self.numerator + O.numerator

        return Fraction(res, self.denominator, co=self.co)

    def sub(self, O: Fraction, *, swap: bool = False) -> Fraction:
        """ Returns N - O, O's detominator must be equal to N's """
        if not isinstance(O, Fraction):
            O = Fraction(numerator=O, denominator=1)

        if O.denominator != self.denominator:
            raise ValueError(f'Denominators must the same, expected {self.denominator} got {O.denominator}')

        if not swap:
            res = self.numerator - O.numerator
        else:
            res = O.numerator - self.numerator

        return Fraction(res, self.denominator, co=self.co)

    def mul(self, O: Fraction) -> Fraction:
        """ Returns N * O """
        if not isinstance(O, Fraction):
            O = Fraction(numerator=O, denominator=1)
        O = O.topHeavy()
        N = self.topHeavy()

        nRes = N.numerator * O.numerator
        dRes = N.denominator * O.denominator

        return Fraction(nRes, dRes)

    def truediv(self, O: Fraction) -> Fraction:
        """ Returns N / O """
        if not isinstance(O, Fraction):
            O = Fraction(numerator=O, denominator=1)

        O = O.flip()

        return self * O

    def __add__(self, O: Fraction) -> Fraction:
        return self.add(O)

    def __sub__(self, O: Fraction) -> Fraction:
        return self.sub(O)

    def __mul__(self, O: Fraction) -> Fraction:
        return self.mul(O)

    def __truediv__(self, O: Fraction) -> Fraction:
        return self.truediv(O)


    def __radd__(self, O: Fraction) -> Fraction:
        return self + O

    def __rsub__(self, O: Fraction) -> Fraction:
        return self.sub(O, swap=True)

    def __rmul__(self, O: Fraction) -> Fraction:
        return self * O

    def __rtruediv__(self, O: Fraction) -> Fraction:
        # No need to swap side
        # in the end it becomes `self * O.flip()`
        # which is the same as `O.flip() * self`
        return self / O

    def __repr__(self) -> str:
        return f'Fraction(numerator={self.numerator} denominator={self.denominator} co={self.co})'
