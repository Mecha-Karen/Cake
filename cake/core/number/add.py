"""
Adding a ``Number`` class with another element
"""
import cake


def _add(N, O, *, return_class = None):
    if hasattr(O, 'value'):
        O = O.value

    if cake.compare_any(N, O, type=(cake.Unknown, cake.Equation)):
        try:
            return N + O if not return_class else return_class(N + O)
        except (ValueError, TypeError):
            return O + N if not return_class else return_class(N + O)

    if cake.compare_any(N, O, type=cake.Expression):
        if hasattr(N, 'expression'):
            return cake.Expression(f'({N.expression}) + {O}')
        return cake.Expression(f'({O.expression}) + {N}')

    try:
        return N + O if not return_class else return_class(N + O)
    except Exception as e:
        raise cake.InvalidObject(f'Cannot add type {N.__class__.__name__} with type {O.__class__.__name__}') from e
