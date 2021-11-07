# Tests for number
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
    

if __name__ == '__main__':
    TestBase()
