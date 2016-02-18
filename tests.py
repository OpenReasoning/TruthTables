from forseti.formula import Symbol
from nose.tools import assert_equal
from nose_parameterized import parameterized, param
import truthtables


def test_symbol():
    symbols, returned = truthtables.runner("A")
    assert_equal(1, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(2, len(returned))
    expected = [[[True], True],
                [[False], False]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


def test_not():
    symbols, returned = truthtables.runner("not(A)")
    assert_equal(1, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(2, len(returned))
    expected = [[[True], False],
                [[False], True]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


def test_and():
    symbols, returned = truthtables.runner("and(A, B)")
    assert_equal(2, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(Symbol("B"), symbols[1])
    assert_equal(4, len(returned))
    expected = [[[True, True], True],
                [[True, False], False],
                [[False, True], False],
                [[False, False], False]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


def test_or():
    symbols, returned = truthtables.runner("or(A, B)")
    assert_equal(2, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(Symbol("B"), symbols[1])
    assert_equal(4, len(returned))
    expected = [[[True, True], True],
                [[True, False], True],
                [[False, True], True],
                [[False, False], False]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


def test_if():
    symbols, returned = truthtables.runner("if(A, B)")
    assert_equal(4, len(returned))
    assert_equal(2, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(Symbol("B"), symbols[1])
    expected = [[[True, True], True],
                [[True, False], False],
                [[False, True], True],
                [[False, False], True]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


def test_iff():
    symbols, returned = truthtables.runner("iff(A, B)")
    assert_equal(4, len(returned))
    assert_equal(2, len(symbols))
    assert_equal(Symbol("A"), symbols[0])
    assert_equal(Symbol("B"), symbols[1])
    expected = [[[True, True], True],
                [[True, False], False],
                [[False, True], False],
                [[False, False], True]]

    for i in range(len(expected)):
        assert_equal(expected[i], returned[i])


@parameterized([
    param([[True], [False]], 1),
    param([[True, True], [True, False], [False, True], [False, False]], 2),
    param([[True, True, True], [True, True, False], [True, False, True],
           [True, False, False], [False, True, True], [False, True, False],
           [False, False, True], [False, False, False]], 3)
])
def test_combinations(expected, num):
    actual = truthtables.get_combinations(num)
    assert_equal(expected, actual)
