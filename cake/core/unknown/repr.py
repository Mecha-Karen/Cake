from .unknown import Unknown    # type: ignore


def _prettify_repr(unk: Unknown) -> str:
    """
    Returns a parsable version of an unknown
    """
    value = unk.value

    raised = unk.data["raised"]
    multip = unk.data["operators"]["multi"]
    div = unk.data["operators"]["div"]
    add = unk.data["operators"]["add"]
    floor = unk.data['operators']['fdiv']
    mod = unk.data['operators']['mod']

    sqrt = unk.data["sqrt"]
    factorial = unk.data["factorial"]
    functions = unk.data['functions']

    STRING = value

    if factorial:
        STRING += "!"

    if raised and raised != 1:
        if isinstance(raised, Unknown):
            raised = f"({str(raised)})"
        else:
            raised = str(raised)
        
        if unk.data.get('MulSwap', False):
            STRING = f"{raised} ** {STRING}"
        else:
            STRING += f" ** {raised}"

    if div:
        if isinstance(div, Unknown):
            div = f"({str(div)})"
        else:
            div = str(div)
        
        if unk.data.get('Dswap', False):
            STRING = f'{div} / {STRING}'
        else:
            STRING += f" / {div}"

    if multip and multip != 1:
        if isinstance(multip, Unknown):
            div = f"({str(div)})"
        else:
            div = str(div)

        if unk.data.get('MulSwap', False):
            STRING = f"{div} * {STRING}"
        else:
            STRING += f" * {div}"

    if add:
        passed = False

        try:
            negated = add < 0
            passed = True
        except Exception:
            pass

        if not passed:
            try:
                negated = getattr(add, "value", 0) < 0
            except TypeError:
                negated = getattr(add, "negated", False)

        if isinstance(add, Unknown):
            val = f"({str(add)})"
        else:
            val = str(add)

        Op = '+'
        if negated or unk.data.get('Aneg', False):
            Op = '-'

        if unk.data.get('Aswap', False):
            STRING = f'{val} {Op} {STRING}'
        else:
            STRING += f' + {val}'

    if floor:
        if isinstance(floor, Unknown):
            floor = f"({str(floor)})"
        else:
            floor = str(floor)

        if unk.data.get('MulSwap', False):
            STRING = f"{floor} // {STRING}"
        else:
            STRING += f" // {floor}"

    if mod:
        if isinstance(mod, Unknown):
            mod = f"({str(mod)})"
        else:
            mod = str(mod)

        if unk.data.get('MulSwap', False):
            STRING = f"{mod} % {STRING}"
        else:
            STRING += f" % {mod}"

    if sqrt:
        STRING = f"sqrt({STRING})"

    for function in functions:
        STRING = f'{function}({STRING})'

    return STRING