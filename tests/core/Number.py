# Basic testing for numbers
import cake

INTEGER_TEST = 10


def TestBase():
    num = cake.Number(INTEGER_TEST)

    print(num, num.value, num.type)
    
    assert num(10)(10) == 1000, "Chaining result for 10 * 10 * 10 didn't return 1000"
    print('Passed chaining test')

    assert num / 10 * 10 + 10 == 20, "Failed BIDMAS"
    print('Passed BIDMAS rig testing')

    assert abs(num) == INTEGER_TEST, "Failed abs method"
    print("Passed ABS testing")

    assert (10 + num) == (INTEGER_TEST + num), "Failed on r operators"
    print('Passed R... dunder operator')

    assert -num == (INTEGER_TEST * -1), "Failed on unary operators"
    print('Passed unary operator')

    # Invert, pos will work fine

    num += INTEGER_TEST
    assert num == (INTEGER_TEST * 2), "Failed on i operators"

    print('Passed I... dunder operator')
    

def testTypeConversion():
    num = cake.Number(INTEGER_TEST)

    integer = cake.Integer(num)
    comp = cake.Complex(20, 6j)
    
    assert integer.type == int, "Incorrect typing for integer class"
    print('Passed Integer Type Testing')

    assert isinstance((10.5 + integer), cake.Float), "Incorrect type conversion"
    print('Passed int + float -> float, test rig')

    assert (num + comp) == cake.Complex(30, 6j), "Failed int -> complex conversion"
    print('Passed int + complex -> complex, test rig')


if __name__ == '__main__':
    TestBase()
    testTypeConversion()
