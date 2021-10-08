# Chaining methods and techniques using cake

# CONTENT:
# LITERAL: L5
# UNKNOWNS: L19
# BRACKETS: L36

from cake import Integer

LITERAL = Integer(10)

# This is the same as doing `x * x`
print( LITERAL(LITERAL) )

# Result: 100

# Getting x cubed can be done using `x * x * x` or
print( LITERAL(LITERAL)(LITERAL) )

# Result: 1000 

from cake import Unknown

x = Unknown("x")

# This is the same as doing `x * x`
print( x(x) )

# Result: Unknown(x²)

# Based off that theory getting `x * x * x` can be done doing
print( x(x)(x) )

# Result: Unknown(x³)

# So now we know how to chain with knowns and unknowns
# How about brackets?
from cake import Integer

x = Integer(10)
y = Integer(20)

z = (x + y)(x)
# This is the same as writing: 30 * 10
print(z)
# Result: 300

# Now with unknowns it gets abit weird
from cake import Unknown, Integer

bracket1 = (Unknown(x) + Integer(10))
# This simplifies to `x + 10`

bracket2 = (Unknown(x) + Integer(10))
# This also simplified to `x + 10`

# So now in essence doing `bracket1 * bracket2`
# Will be the same as: (Unknown(x) + Integer(10))(Unknown(x) + Integer(10))
# Correct!

# Just like in normal mathmatics it will do
# x * x -> x ** 2
# x * 10 -> 10x
# 10 * x -> 10x
# 10 * 10 -> 100

# -> x**2 + 20x + 100

print(bracket1 * bracket2)
# Result: Unknown(x² + 20x + 100)
# You can directly filter this object through a `Quadratic` object and preform some nice calcs
