<h1 align="center">Cake</h1>
<p align="center">An object orientated math library, Built with power and simplicity!</p>

<p>
    Cake is an object orientated math library based off <strong>Sympy</strong> and aims to be simple and easy to use. Its main advantages are easy of use, chaining and provides shortcuts to lengthy methods.<br><br>
    License: MIT License (see the LICENSE file for details) covers all files in the <strong>cake</strong> repository unless stated otherwise.
</p>

<h2>Features</h2>
<ul>
    <li>Generally is fast and provides simple solutions for complex problems</li>
    <li>Simple to use and learn</li>
    <li>Provides support for algebra and equation substitution</li>
</ul>

<h2>Installation</h2>
This library is currently in very early works! It does not have much to offer as of now, but we have a vision to make it full of features!

<h3>Stable</h3>

```sh
# Windows
pip install MathCake

# Linux/MacOS
pip3 install MathCake
```

<h3>Development</h3>

```sh
git clone https://github.com/Mecha-Karen/Cake
cd Cake
pip install .
```

<h2>Documentation</h2>

To compile the documentation, click [me](https://github.com/Mecha-Karen/Documentation#compiling-cake)for more information

If you wish to view the live version, click [me](https://docs.mechakaren.xyz/cake).

<h2>Quick Example</h2>

<h3>Quadratic Formula</h3>
Note: This is currently just a concept!

```py
from cake import Expression

expr = Expression("-b (+|-) sqrt((b ** 2) - 4(a)(c))")
# Top layer of the formula

# (+|-) will return 2 solutions as stated in the documentation
# Its one of the many ways of implements plus or minus

expr.wrap_all("/", "2(a)")
# Puts the entire current formula into brackets and divides by 2a

print(expr.substitute(a=10, b=-20, c=5))

# Results: (1.70711, 0.292893)
```

<h2>Links</h2>
<ul>
    <li><a href="https://docs.mechakaren.xyz/cake">Documentation</a></li>
    <li><a href="https://discord.gg/Q5mFhUM">Support Server</a></li>
    <li><a href="https://pypi.org/project/MathCake/">PyPi Page</a></li>
</ul>