from setuptools import setup, find_packages
import re

version = ""

with open("cake/__init__.py") as f:
    contents = f.read()

    _match = re.search(
        r'^__version__\s*=\s*[\'"]([^\'"]*)[\'"]', contents, re.MULTILINE
    )

    version = _match.group(1)

if not version:
    raise RuntimeError("Cannot resolve version")


classifiers = [
    "Development Status :: 1 - Planning",
    "Intended Audience :: Developers",
    "Operating System :: OS Independent",
    "License :: OSI Approved :: MIT License",
    "Programming Language :: Python :: 3",
]

setup(
    name="MathCake",
    version=version,
    description="An object orientated math library",
    long_description=open("README.md").read(),
    long_description_content_type="text/markdown",
    url="https://github.com/Mecha-Karen/Cake",
    project_urls={
        "Documentation": "https://docs.mechakaren.xyz/cake",
        "Issue tracker": "https://github.com/Mecha-Karen/Cake/issues",
        "Organisation": "https://github.com/Mecha-Karen",
    },
    author="Mecha Karen",
    license="MIT License",
    classifiers=classifiers,
    keywords="Math,Python3,OOP",
    packages=find_packages(),
    install_requires=[],
)
