"""
Operations for a ``Number`` class
"""
import cake
import operator

operator.divmod = divmod
# Add divmod function to operator interface


def evaluate(N, O, *, return_class = None, func: str = 'add'):
    """
    Evaluate 2 tokens, if implementing in custom class, N will be self/current value

    Parameters
    ----------
    N: :class:`~typing.Any`
        First token
    O: :class:`~typing.Any`
        Second token
    return_class: :class:`~typing.Callable`
        A function or class to be returned after evaluating the tokens, else returns the evaluated tokens
    func: :class:`str`
        The name of the operation, check out the ``operator`` module
    """
    if hasattr(O, 'value'):
        O = O.value
    if hasattr(O, 'get_value'):
        O = O.get_value()
    
    if isinstance(func, str):
        func = getattr(operator, func)

    if cake.compare_any(N, O, type=(cake.Unknown, cake.Equation)):
        try:
            return func(N, O) if not return_class else return_class(func(N, O))
        except (ValueError, TypeError):
            return func(O, N) if not return_class else return_class(func(O, N))

    if cake.compare_any(N, O, type=cake.Expression):
        if hasattr(N, 'expression'):
            if isinstance(O, cake.Expression):
                O = O.expression
            return cake.Expression(f'({N.expression}) + {O}')
            
        if isinstance(N, cake.Expression):
            N = N.expression
        return cake.Expression(f'({O.expression}) + {N}')

    try:
        return func(O, N) if not return_class else return_class(func(O, N))
    except Exception as e:
        raise cake.InvalidObject(f'Cannot add type {N.__class__.__name__} with type {O.__class__.__name__}') from e
