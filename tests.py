# -*- coding: utf-8 -*-
# pylint: disable=missing-docstring

from __future__ import unicode_literals
from forseti.formula import Symbol, Not, And, Or, If, Iff, Predicate
from nose import runmodule
from nose.tools import assert_equal, raises
from parameterized import parameterized
import sys
import truthtables


PYTHON_2 = sys.version_info[0] == 2


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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


def test_or():
    table = truthtables.runner(str("or(A, B)"))
    assert_equal([[[True, True, True]], [[True, True, False]], [[False, True, True]],
                  [[False, False, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), Or(Symbol("A"), Symbol("B")), Symbol("B")]], table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[True]], [[True]], [[False]]], table.connective_evaluation)
    assert_equal([[True], [True], [True], [False]], table.evaluation)
    assert_equal([Or(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


def test_if():
    table = truthtables.runner(str("if(A, B)"))
    assert_equal([[[True, True, True]], [[True, False, False]], [[False, True, True]],
                  [[False, True, False]]], table.broken_evaluation)
    assert_equal([[Symbol("A"), If(Symbol("A"), Symbol("B")), Symbol("B")]], table.broken_formulas)
    assert_equal([[True, True], [True, False], [False, True], [False, False]], table.combinations)
    assert_equal([[[True]], [[False]], [[True]], [[True]]], table.connective_evaluation)
    assert_equal([[True], [False], [True], [True]], table.evaluation)
    assert_equal([If(Symbol("A"), Symbol("B"))], table.formulas)
    assert_equal([[1, 0]], table.main_connective_index)
    assert_equal([Symbol("A"), Symbol("B")], table.symbols)
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


def test_iff():
    table = truthtables.runner(str("iff(A, B)"))
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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


def test_not_and():
    table = truthtables.runner(str("not(and(A, B))"))
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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])

    if not PYTHON_2:
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
    table = truthtables.runner(str("and(not(or(A, C)), B)"), display_connectives=False)
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
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])

    if not PYTHON_2:
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


def test_tautology():
    table = truthtables.runner("or(A,not(A))")
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is a Tautology", table.get_table_assessment()[0])


def test_contradiction():
    table = truthtables.runner("and(A,not(A))")
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is a Contradiction", table.get_table_assessment()[0])


def test_empty_statements():
    table = truthtables.runner(["A", ''])
    assert_equal([[[True]], [[False]]], table.broken_evaluation)
    assert_equal([[Symbol("A")]], table.broken_formulas)
    assert_equal([[True], [False]], table.combinations)
    assert_equal([[[]], [[]]], table.connective_evaluation)
    assert_equal([[True], [False]], table.evaluation)
    assert_equal([Symbol("A")], table.formulas)
    assert_equal([[]], table.main_connective_index)
    assert_equal([Symbol("A")], table.symbols)
    assert_equal(1, len(table.get_table_assessment()))
    assert_equal("Sentence is TT-Possible", table.get_table_assessment()[0])


def test_set_1():
    table = truthtables.runner(["A", "A"])
    assert_equal([[[True], [True]], [[False], [False]]], table.broken_evaluation)
    assert_equal([[Symbol("A")], [Symbol("A")]], table.broken_formulas)
    assert_equal([[True], [False]], table.combinations)
    assert_equal([[[], []], [[], []]], table.connective_evaluation)
    assert_equal([[True, True], [False, False]], table.evaluation)
    assert_equal([Symbol("A"), Symbol("A")], table.formulas)
    assert_equal([[], []], table.main_connective_index)
    assert_equal([Symbol("A")], table.symbols)
    assert_equal(4, len(table.get_table_assessment()))


def test_set_2():
    table = truthtables.runner(["A", "B"])
    assert_equal(1, len(table.get_table_assessment()))


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
    (Symbol('a'), 'a'),
    (Not(Symbol('a')), '¬a'),
    (And(Symbol('a'), Symbol('b')), '(a ∧ b)'),
    (Or(Symbol('a'), Symbol('b')), '(a ∨ b)'),
    (If(Symbol('a'), Symbol('b')), '(a → b)'),
    (Iff(Symbol('a'), Symbol('b')), '(a ↔ b)'),
    (Not(And(
        Symbol('a'),
        If(Symbol('c'), Iff(Or(Symbol('d'), Symbol('a')), Symbol('c')))
    )), '¬(a ∧ (c → ((d ∨ a) ↔ c)))')
])
def test_pretty_print(formula, expected):
    assert_equal(expected, truthtables.pretty_print(formula))


@raises(TypeError)
def test_pretty_print_raises():
    class Foo(Predicate):
        name = "not"
        arity = 1
    truthtables.pretty_print(Foo)


@parameterized([
    ([[True], [False]], 1),
    ([[True, True], [True, False], [False, True], [False, False]], 2),
    (
        [
            [True, True, True], [True, True, False], [True, False, True],
            [True, False, False], [False, True, True], [False, True, False],
            [False, False, True], [False, False, False]
        ],
        3
    )
])
def test_combinations(expected, num):
    actual = truthtables.get_combinations(num)
    assert_equal(expected, actual)


if __name__ == "__main__":
    runmodule()
