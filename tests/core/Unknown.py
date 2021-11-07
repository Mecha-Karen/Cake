# Basic testing for unknowns
import cake

BASE = cake.Unknown('x')

def testBase():
    assert repr(BASE + 10) == 'x + 10', "Addition failed"
    assert repr(BASE - 10) == 'x + -10', "Subtraction failed"   # May need to simplify it later
    assert repr(10 - BASE) == '10 - x', "Subtraction O - N, failed"
    assert repr(BASE * BASE) == 'x ** 2', "Power failed"
    assert repr(BASE / BASE) == 'x / (x)', "Division failed"    # Evaluates the x from brack first
    

def testTermMultiplication():
    BS = BASE.copy()
    # x
    BS += 20
    # x + 20
    BS *= BASE
    # x ** 2 + 20x

    # same as x(x + 20)
    # x * x -> x ** 2
    # x * 20 -> 20x
    # And add then your done

    print(BS)

if __name__ == '__main__':
    testBase()
    testTermMultiplication()
