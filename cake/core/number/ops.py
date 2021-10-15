"""
Operations for a ``Number`` class
"""
import cake
import operator

operator.divmod = divmod
# Add divmod function to operator interface


def evaluate(N, O, *, return_class = None, func: str = 'add'):
    if hasattr(O, 'value'):
        O = O.value
    if isinstance(func, str):
        func = getattr(operator, func)

    if cake.compare_any(N, O, type=(cake.Unknown, cake.Equation)):
        try:
            return func(N, O) if not return_class else return_class(func(N, O))
        except (ValueError, TypeError):
            return func(O, N) if not return_class else return_class(func(O, N))

    if cake.compare_any(N, O, type=cake.Expression):
        if hasattr(N, 'expression'):
            return cake.Expression(f'({N.expression}) + {O}')
        return cake.Expression(f'({O.expression}) + {N}')

    try:
        return func(O, N) if not return_class else return_class(func(O, N))
    except Exception as e:
        raise cake.InvalidObject(f'Cannot add type {N.__class__.__name__} with type {O.__class__.__name__}') from e
