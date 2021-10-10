# Getting started with algebra using cake

# Import symbols or the Unknown object
from cake import symbols
from cake import Unknown

# Unknown:
x = Unknown("x")
# Unknown(x)

# If your lazy with methods you can use the `.parse` method
x = Unknown.parse("x ** 2")
# Unknown(x²)

# Symbols function
x = symbols(x)
# Returns the same result as using the Object directly
# Except you no longer have the privilege of the `parse` utility

# Do some simple methods
x += 10

# Unknown(10 + x)

# Substitute a new value in
print(x.substitute(10))

# Integer(20)
