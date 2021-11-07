# CLI for running tests in cake
import argparse
import os
import pathlib
import subprocess
import time
import traceback

ERROR = "\x1b[91m"
SUCCESS = "\x1b[92m"
INFO = "\x1b[96m"
RESET = "\x1b[39m"
FILL = "█"
LINE_SEP = '-' * 100

print(RESET)

def ProgressBar(iteration, total, 
    prefix = '', suffix = '', decimals = 1, length = 100, fill = FILL, printEnd = "\r"
):
    completePercent = ("{0:." + str(decimals) + "f}").format(100 * (iteration / float(total)))
    filledLength = int(length * iteration // total)
    bar = fill * filledLength + '-' * (length - filledLength)
    print(f'\r{prefix} |{bar}| {completePercent}% {suffix}', end = printEnd)
    # Print New Line on Complete
    if iteration == total: 
        print()

def runFile(file, *, timeout: int = 300):
    path = file.absolute()

    if isinstance(path, pathlib.WindowsPath):
        py = 'python'
    else:
        py = 'python3'

    start = time.perf_counter()
    print(f'{INFO}[INFO] | Testing - \n{path}\n{LINE_SEP}')

    proc = subprocess.Popen(
        [py, path],
        shell=False,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
    )

    try:
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired as exc:
        exc = traceback.format_exception(etype=type(exc), value=exc, tb=exc.__traceback__)
        error = ''.join(exc)
    else:
        stderr = proc.stderr
        stderr.seek(0)
        error = stderr.read(-1)

        stderr.close()

    failed = proc.returncode == 1

    if failed:
        ERROR_STACK.update({file: error.decode()})
        print(f'\n{ERROR}[ERROR] | Encountered error during test, Writing error to log file{RESET}')
    else:
        stdout = proc.stdout
        stdout.seek(0)
        output = stdout.read(-1)

        stdout.close()

        output = output.decode().strip()

        print(f'{SUCCESS} [Test Completed] | Your test completed with 0 errors - Output:{RESET}\n{output}')
    
    ms = (time.perf_counter() - start) * 1000

    print(f'\nTest completed in {ms}ms')
    print(LINE_SEP)

parser = argparse.ArgumentParser()
BASE_PATH = pathlib.Path('./run.py')

ERROR_STACK = dict()

parser.add_argument(
    '-a', '--all',
    help="Run all tests in the tests folder",
    type=bool,
)

parser.add_argument(
    '-i', '--ignore', default=[],
    nargs='+', type=str,
    help="Ignore a certain files or folders"
)

parser.add_argument(
    '--I', '-include', default=[],
    nargs='+', type=str,
    help="Include a set of files"
)

parser.add_argument(
    '-t', '-timeout', 
    default=300, type=int,
    help="Change timeout for each test, defaults to 300"
)

args = parser.parse_args()
TIMEOUT = args.t

# Files all .py files
files = list(pathlib.Path('./').rglob('**/*.py'))

for file in files:
    if file == BASE_PATH:
        files.remove(file)
    elif str(file) in args.ignore:
        files.remove(file)

if not args.all and getattr(args, 'include', False):
    files = [file for file in files if str(file) in args.include]

if not files:
    print(f'{INFO} [INFO] | No files were provided to test, killing process', RESET)
    os._exit(0)
print(f'{INFO}[INFO] | Testing {len(files)} files{RESET}\n')


ProgressBar(0, len(files), prefix="Progress:", suffix="Completed")

for i, file in enumerate(files):
    runFile(file, timeout=TIMEOUT)
    ProgressBar(i + 1, len(files), prefix="Progress:", suffix="Completed")

if ERROR_STACK:

    if not os.path.isdir('./errors'):
        os.mkdir('./errors')
        print(
            f'{INFO}Created errors directory -\n{os.path.abspath("./errors")}', 
            RESET
        )

    ProgressBar(0, len(ERROR_STACK), prefix="Progress:", suffix="Completed")

    for i, key in enumerate(ERROR_STACK):
        file = key
        error = ERROR_STACK[file]

        with open(f'./errors/{file.name}.log', 'w') as f:
            f.write(f'Error from "{file.absolute()}"\n\n{error}')
        ProgressBar(i + 1, len(ERROR_STACK), prefix="Progress:", suffix="Completed")

print(
    f'{SUCCESS} [Completed] Test completed, with {len(ERROR_STACK)} errors, from {len(files)} files', 
    RESET
)


print(RESET)    # Just incase colour still exists
