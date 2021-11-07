# Basic testing for unknowns
import cake

BASE = cake.Unknown('x')

def testBase():
    assert repr(BASE + 10) == 'x + 10', "Addition failed"
    assert repr(BASE - 10) == 'x + -10', "Subtraction failed"   # May need to simplify it later
    assert repr(10 - BASE) == '10 - x', "Subtraction O - N, failed"
    assert repr(BASE * BASE) == 'x ** 2', "Power failed"
    assert repr(BASE / BASE) == 'x / (x)', "Division failed"    # Evaluates the x from brack first
    

if __name__ == '__main__':
    testBase()
