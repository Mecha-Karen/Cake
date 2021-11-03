.. meta::
    :title: Documentation - Mecha Karen
    :type: website
    :url: https://docs.mechakaren.xyz/
    :description: Cake - Functions [Guides]
    :theme-color: #f54646

*********
Functions
*********
Hello there! Welcome to cakes functions guide. This will show you everything you can do with functions and how they work!

What is a function?
-------------------
A function is a class which evaluates a specific input value and returns an output.

Example Functions
-----------------
Some of the built-in functions that come with cake are Sin, Tan and Sqrt. All of the functions from the standard math library are included.

Import Patterns
^^^^^^^^^^^^^^^

.. code-block:: py

    >>> from cake import Sqrt
    >>> from cake import sqrt
    # sqrt => math.sqrt
    # Sqrt => cake.Sqrt

To import a function from the math lib, simply lowercase your import. For the cake version of camel-case the import.

Using Functions
===============
Intialising functions will return the function in its class form as opposed to returning the result, to evaluated your function you need to call the initiated function.

Example
^^^^^^^

.. code-block:: py

    >>> from cake import Sin
    >>> func = Sin(90)
    >>> func
    Sin(functions=[] handler=MaskFunctionTemp._raw_exec execAfter=None is_multi=False value=90)
    >>> func()
    Real(1.0)


Combining Functions
===================
To combine functions you need to pass the intialised func through as the value.
It will evaluate the functions from left to right. So it will start with `N` then `O`. 

In the example provided below, it evaluated Sin before passing it through Cos

If your function `X` has function `Y` and `X` is passed through `Z`.
The evaluation tree may look like:

.. code-block:: text

    Z -> CALL X
    X -> CALL Y

    X.value = exec(y)
    X.value = X.handler(X.value)
    Z.value = Z.handler(X.value)

    return Z

Example
^^^^^^^

.. code-block:: py

    >>> from cake import Sin, Cos
    >>> x = Sin(90)
    >>> x
    Sin(functions=[] handler=MaskFunctionTemp._raw_exec execAfter=None is_multi=False value=90)
    >>> y = Cos(x)
    >>> y
    Cos(functions=[Sin(...)] ...)
    >>> y()
    Real(0.9998476951563913)

Creating Functions
==================
For creating functions it is recomended to use the ``Function`` or ``MaskFunctionTemp`` class.
You may also use the ``FunctionBase`` class, which may require lengthier function codes.

FunctionBase Class
^^^^^^^^^^^^^^^^^^

.. code-block:: py

    from cake import FunctionBase

    class MyFunc(FunctionBase):
        def __init__(self, value) -> None:
            super().__init__("MyFunc", lambda x: x + 1)

    val = 10
    func = MyFunc(val)
    result = func()
    print(result)

Function Class
^^^^^^^^^^^^^^
You can see the example for the function class <here `https://github.com/Mecha-Karen/Cake/blob/main/examples/functions.py`>_

MaskFunctionTemp Class
^^^^^^^^^^^^^^^^^^^^^^
This class should only be used for external handlers, which already exist, else just implement the ``Function`` class for increased flexibility.

.. code-block:: py

    from cake import MaskFunctionTemp
    from cake import sin

    class Sin(MaskFunctionTemp):
        def __init__(self, value, *, type: str = "radians") -> None:
            super().__init__(value, "sin", math.sin, type=type)

    x = Sin(90)
    result = x()
    print(result)
