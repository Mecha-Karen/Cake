.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Cake - Equation [API Ref]
    :theme-color: #f54646

.. currentmodule:: cake

********
Equation
********
A class which simply states, ``expr1 = expr2``.

.. warning::

    This class must not be directly used in an ``if`` statement, when creating one from an ``Expression`` object.

    .. code-block:: py

        >>> if (Expr == ...):
                ...

        # This is wrong!
        # It will ALWAYS be true
        # Instead try something like

        >>> if (Expr == ...).solve(*args, **kwargs) == ...:
                ...

        # This is saying, that if the solved equation is equal to something
        # Instead of saying ``if Equation:``


.. autoclass:: cake.Equation
    :members: