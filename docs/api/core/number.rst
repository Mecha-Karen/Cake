.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Cake - Number class [API Ref]
    :theme-color: #f54646

.. currentmodule:: cake

.. _NumberClass:

******
Number
******

.. autoclass:: cake.Number
    :members:
    :exclude-members: set_value, remove_value, set_type

    .. rubric:: Dunder Methods

    .. autosummary::

        ~cake.Number.__call__
        ~cake.Number.__abs__
        ~cake.Number.__add__
        ~cake.Number.__sub__
        ~cake.Number.__neg__
        ~cake.Number.__pos__
        ~cake.Number.__mul__
        ~cake.Number.__ceil__
        ~cake.Number.__truediv__
        ~cake.Number.__floordiv__
        ~cake.Number.__mod__
        ~cake.Number.__divmod__
        ~cake.Number.__pow__
        ~cake.Number.__lshift__
        ~cake.Number.__rshift__
        ~cake.Number.__and__
        ~cake.Number.__xor__
        ~cake.Number.__or__
        ~cake.Number.__lt__
        ~cake.Number.__le__
        ~cake.Number.__gt__
        ~cake.Number.__ge__
        ~cake.Number.__eq__
        ~cake.Number.__ne__
        ~cake.Number.__bool__
        ~cake.Number.__int__
        ~cake.Number.__float__
        ~cake.Number.__complex__
        ~cake.Number.__str__

    .. method:: get_value(self, other, check_value_attr, *args, **kwargs)

        Get the value of other by checking if O has either, a ``get_value`` method or a ``value`` attr.

        .. note::

            If O is ``None``, O becomes N
