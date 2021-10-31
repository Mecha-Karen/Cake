# Parsing Helpers
import ast
import typing
from typing import (
    Any, List, Tuple, Union, Dict
)

EVAL_FUNCTION_NAME = "CakeWorker"
# Function name for running the generated code

LINE_SEP = '\n'
# Fixes error with backlash in f statement


def GEN_AUTO_CODE_MARKING(*imports):
    # Generates the comments and imports the cake library
    Newimports = list()

    for _import in imports:
        lib, *extras = _import.split(' ')
        extras = ' '.join(extras)
        Newimports.append(f'from {lib} import {extras}')

    import time
    return f"""\
# This code was generated using `Cakes` auto generator at {time.strftime("%d/%m/%Y (%I:%M %p)")}
# This code may not be perfect, it may have bugs. Don't be fustrated. Just submit an issue!
# You can modify any of this code to your liking

# Source: https://github.com/Mecha-Karen/Cake
# Copyright: Mecha Karen (2021 - Present)
    
from cake import *\n
{LINE_SEP.join(Newimports)}"""


def getEvalBody(code: Union[List[str], str], *imports) -> Tuple[str, List[str]]:
    if not isinstance(code, list):
        code = code.splitlines()

    code = code[(8 + len(imports)):]

    code[-1] = f"locals()['result'] = {code[-1]}"

    code = '\n'.join(code)

    _ModImports = list()

    for importedModule in imports:
        lib, *extras = importedModule.split(' ')
        extras = ' '.join(extras)
        _ModImports.append(f'from {lib} import {extras}')

    return code, _ModImports


def execCode(code: str, *, local: dict = {}) -> typing.Any:
    evalBody, imports = getEvalBody(code)

    imports.insert(0, 'from cake import *')
    globDict: Dict[str, Any] = dict()

    for _import in imports:
        exec(_import, globDict)

    astParsed = ast.parse(evalBody, mode="exec")
    cc = compile(astParsed, "<ast>", "exec")

    exec(cc, globDict, local)
    return local['result']
