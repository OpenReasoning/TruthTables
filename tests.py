# pylint: disable=missing-docstring

from forseti.formula import Symbol, Not, And, Or, If, Iff
from nose import run as nose_run
from nose.tools import assert_equal, raises
from nose_parameterized import parameterized, param
import truthtables


def test_symbol():
    table = truthtables.runner("A")
    assert_equal([[[True]], [[False]]], table.broken_evaluation)
    assert_equal([[Symbol("A")]], table.broken_formulas)
    assert_equal([[True], [False]], table.combinations)
    assert_equal([[[]], [[]]], table.connective_evaluation)
    assert_equal([[True], [False]], table.evaluation)
    assert_equal([Symbol("A")], table.formulas)
    assert_equal([[]], table.main_connective_index)
    assert_equal([Symbol("A")], table.symbols)


def test_not():
    table = truthtables.runner("not(A)")
    assert_equal([[[False, True]], [[True, False]]], table.broken_evaluation)
    assert_equal([[Not(Symbol("A")), Symbol("A")]], table.broken_formulas)
    assert_equal([[True], [False]], table.combinations)
    assert_equal([[[False]], [[True]]], table.connective_evaluation)
    assert_equal([[False], [True]], table.evaluation)
    assert_equal([Not(Symbol("A"))], table.formulas)
    assert_equal([[0, 0]], table.main_connective_index)
    assert_equal([Symbol("A")], table.symbols)


def test_and():
    table = truthtables.runner("and(A, B)")
    assert_equal([[[True, True, True]], [[True, False, False]], [[False, False, True]],
                  [[False, False, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), And(Symbol("A"), Symbol("B")), Symbol("B")]],
                 table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[False]], [[False]], [[False]]], table.connective_evaluation)
    assert_equal([[True], [False], [False], [False]], table.evaluation)
    assert_equal([And(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)


def test_or():
    table = truthtables.runner("or(A, B)")
    assert_equal([[[True, True, True]], [[True, True, False]], [[False, True, True]],
                  [[False, False, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), Or(Symbol("A"), Symbol("B")), Symbol("B")]], table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[True]], [[True]], [[False]]], table.connective_evaluation)
    assert_equal([[True], [True], [True], [False]], table.evaluation)
    assert_equal([Or(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)


def test_if():
    table = truthtables.runner("if(A, B)")
    assert_equal([[[True, True, True]], [[True, False, False]], [[False, True, True]],
                  [[False, True, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), If(Symbol("A"), Symbol("B")), Symbol("B")]], table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[False]], [[True]], [[True]]], table.connective_evaluation)
    assert_equal([[True], [False], [True], [True]], table.evaluation)
    assert_equal([If(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)


def test_iff():
    table = truthtables.runner("iff(A, B)")
    assert_equal([[[True, True, True]], [[True, False, False]], [[False, False, True]],
                  [[False, True, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), Iff(Symbol("A"), Symbol("B")), Symbol("B")]],
                 table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[False]], [[False]], [[True]]], table.connective_evaluation)
    assert_equal([[True], [False], [False], [True]], table.evaluation)
    assert_equal([Iff(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)


def test_not_and():
    table = truthtables.runner("not(and(A, B))")
    assert_equal([[[False, True, True, True]], [[True, True, False, False]],
                  [[True, False, False, True]], [[True, False, False, False]]],
                 table.broken_evaluation)
    assert_equal([[Not(And(Symbol("A"), Symbol("B"))), Symbol("A"), And(Symbol("A"), Symbol("B")), Symbol("B")]],
                 table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[False, True]], [[True, False]], [[True, False]], [[True, False]]],
                 table.connective_evaluation)
    assert_equal([[False], [True], [True], [True]], table.evaluation)
    assert_equal([Not(And(Symbol("A"), Symbol("B")))], table.formulas)
    assert_equal([[0, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)


def test_and_or():
    table = truthtables.runner("and(or(A, C), or(B,C))")
    # A or C and B or C
    assert_equal([[[True, True, True, True, True, True, True]],
                  [[True, True, False, True, True, True, False]],
                  [[True, True, True, True, False, True, True]],
                  [[True, True, False, False, False, False, False]],
                  [[False, True, True, True, True, True, True]],
                  [[False, False, False, False, True, True, False]],
                  [[False, True, True, True, False, True, True]],
                  [[False, False, False, False, False, False, False]]],
                 table.broken_evaluation)
    assert_equal([[Symbol("A"), Or(Symbol("A"), Symbol("C")), Symbol("C"),
                   And(Or(Symbol("A"), Symbol("C")), Or(Symbol("B"), Symbol("C"))), Symbol("B"),
                   Or(Symbol("B"), Symbol("C")), Symbol("C")]], table.broken_formulas)
    assert_equal([[True, True, True], [True, True, False], [True, False, True],
                  [True, False, False], [False, True, True], [False, True, False],
                  [False, False, True], [False, False, False]], table.combinations)
    assert_equal([[[True, True, True]], [[True, True, True]], [[True, True, True]],
                  [[True, False, False]], [[True, True, True]], [[False, False, True]],
                  [[True, True, True]], [[False, False, False]]],
                 table.connective_evaluation)
    assert_equal([[True], [True], [True], [False], [True], [False], [True], [False]],
                 table.evaluation)
    assert_equal([And(Or(Symbol("A"), Symbol("C")), Or(Symbol("B"), Symbol("C")))], table.formulas)
    assert_equal([[3, 1]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B"), Symbol("C")], table.symbols)

    assert_equal("A B C | ((A ∨ C) ∧ (B ∨ C))\n" +
                 "---------------------------\n" +
                 "T T T |     T   -T    T    \n" +
                 "T T F |     T   -T    T    \n" +
                 "T F T |     T   -T    T    \n" +
                 "T F F |     T   -F    F    \n" +
                 "F T T |     T   -T    T    \n" +
                 "F T F |     F   -F    T    \n" +
                 "F F T |     T   -T    T    \n" +
                 "F F F |     F   -F    F    \n", table.generate_table())


def test_and_not_or():
    table = truthtables.runner("and(not(or(A, C)), B)", display_connectives=False)
    assert_equal([[[False, True, True, True, False, True]],
                  [[False, True, True, False, False, True]],
                  [[False, True, True, True, False, False]],
                  [[False, True, True, False, False, False]],
                  [[False, False, True, True, False, True]],
                  [[True, False, False, False, True, True]],
                  [[False, False, True, True, False, False]],
                  [[True, False, False, False, False, False]]],
                 table.broken_evaluation)
    assert_equal([[Not(Or(Symbol("A"), Symbol("C"))), Symbol("A"), Or(Symbol("A"), Symbol("C")),
                   Symbol("C"), And(Not(Or(Symbol("A"), Symbol("C"))), Symbol("B")), Symbol("B")]],
                 table.broken_formulas)
    assert_equal([[True, True, True], [True, True, False], [True, False, True],
                  [True, False, False], [False, True, True], [False, True, False],
                  [False, False, True], [False, False, False]], table.combinations)
    assert_equal([[[False, True, False]], [[False, True, False]], [[False, True, False]],
                  [[False, True, False]], [[False, True, False]], [[True, False, True]],
                  [[False, True, False]], [[True, False, False]]],
                 table.connective_evaluation)
    assert_equal([[False], [False], [False], [False], [False], [True], [False], [False]],
                 table.evaluation)
    assert_equal([And(Not(Or(Symbol("A"), Symbol("C"))), Symbol("B"))], table.formulas)
    assert_equal([[4, 2]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B"), Symbol("C")], table.symbols)

    assert_equal("A B C | (¬(A ∨ C) ∧ B)\n" +
                 "----------------------\n" +
                 "T T T |          -F   \n" +
                 "T T F |          -F   \n" +
                 "T F T |          -F   \n" +
                 "T F F |          -F   \n" +
                 "F T T |          -F   \n" +
                 "F T F |          -T   \n" +
                 "F F T |          -F   \n" +
                 "F F F |          -F   \n", table.generate_table())


@raises(TypeError)
def test_truthtables_runner_invalid_type():
    truthtables.runner(1)


@raises(TypeError)
def test_truthtables_invalid_type():
    truthtables.TruthTable(1)


@raises(TypeError)
def test_truthtables_invalid_type_list():
    truthtables.TruthTable([1])


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

if __name__ == "__main__":
    nose_run()
