# Creating and using functions in `cake`
# Lets start off with using pre-made functions

from cake import Tan, Cos
# All functions from cake are the same in the math library
# You can import the normal functions by just lowercasing the import names
# e.g. `from cake import tan` imports the normal function (math.tan)

x = Tan(10)
# This will return the function, to get your value just call it
# By default this convers 10 to radians, to use degrees specify the `type` kwarg
# Example: `Tan(10, type="degrees")`
print(x())
# Result: Real(0.17632698070846498)

# Integerating multiple functions
# Simple pass the other function through as an arg
# All the functions in `other` will be evaluated with this one as well
y = Cos(x)
# Cos(functions=[Tan(functions=[] handler=Tan._raw_exec is_multi=False)] handler=Cos._raw_exec is_multi=True)
print(y)
# Real(0.017455064928217585)

# Now lets create our own function
from cake import Function

class MyFunc(Function):
    def __init__(self, value) -> None:
        super().__init__(value, name="My Function")
    
    def _raw_exec(self, other):
        return other + 5

# Thats it!
# You have created your own function
# Lets use it now

x = MyFunc(10)
print(x())
# 15

# You can even thread your own function into built-in functions
y = Cos(x)
# Cos(functions=[My Function(functions=[] handler=MyFunc._raw_exec is_multi=False)] handler=Cos._raw_exec is_multi=True)

print(y())
# Real(0.9659258262890683)

# Playing with the type conversion in built in functions
# Lets say you have your own type converter and you dont like to use `radians` or `degrees`
# Simply add it to the built-in `math` library and pass the name through!
from cake import Tan
import math

# Simple example, just negating the number
def myConverter(number: int) -> int:
    return number * -1

math.myConverter = myConverter

x = Tan(10, type="myConverter")
print(x())
# Real(-0.6483608274590866)

# Easy as that!
