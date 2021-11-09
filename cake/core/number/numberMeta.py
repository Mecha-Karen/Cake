""" Metaclass for number classes """
from abc import ABCMeta, abstractmethod


class Number_(metaclass=ABCMeta):
    """
    All number classes must inherit this.
    This is mainly because if you wish to check if an object is a number.
    You just need to simply do

    .. codeblock:: py

        >>> from cake import Number_, Integer
        >>> isinstance(Integer(10), Number_)
        True
        
    """
    __slots__ = ()
