.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Cake - API Reference
    :theme-color: #f54646

.. currentmodule:: cake

*************
API Reference
*************
The API Reference for our modules, as well as a few other categories, are outlined in the following section.

.. note::
    This module strongly uses the concept of ``chaining``. This allows for a more mathmatically correct statements such as
    
    .. code-block:: py

        >>> from cake import Integer
        >>> Integer(10)(10)(10)
        Integer(1000)

Information about the version
=============================
.. data:: version_info

    A named tuple that is similar to :obj:`py:sys.version_info`.

    Just like :obj:`py:sys.version_info` the valid values for ``releaselevel`` are
    'Pre-Alpha', 'Alpha', 'Beta', 'Stable' and 'Final'.

Pages
=====

.. toctree::
    :titlesonly:
    :caption: Core

    core/number
    core/types
    core/surd

.. toctree::
    :titlesonly:
    :caption: Parsing

    parsing/equation
    parsing/expression
