# -*- coding: utf-8 -*-

"""
Module for generating Truth Tables for logical formulas
"""

from __future__ import print_function, unicode_literals
import argparse
from six import string_types
import forseti.parser
from forseti.formula import Formula, Symbol, Predicate, Not, And, Or, If, Iff


def evaluate_formula(formula, symbols, combination):
    """

    :param formula:
    :param symbols:
    :param combination:
    :return:
    """
    if isinstance(formula, Symbol) or isinstance(formula, Predicate):
        return combination[symbols.index(formula)]
    elif isinstance(formula, Not):
        return not evaluate_formula(formula.args[0], symbols, combination)
    else:
        args = []
        for i in range(len(formula.args)):
            args.append(
                evaluate_formula(formula.args[i], symbols, combination)
            )
        if isinstance(formula, And):
            return False not in args
        elif isinstance(formula, Or):
            return True in args
        elif isinstance(formula, If):
            return not (args[0] is True and args[1] is False)
        elif isinstance(formula, Iff):
            return args[0] == args[1]


def get_combinations(num):
    """
    Generate all True/False combinations for a given number

    :param num:
    :return:
    """
    temp = [True] * num
    combinations = []
    i = 0
    while i < 2 ** num:
        combinations.append(temp[::-1])
        for j in range(len(temp)):
            if temp[j] is True:
                temp[j] = False
                break
            else:
                temp[j] = True
        i += 1
    return combinations


def pretty_print(formula):
    """

    :param formula:
    :return:
    """
    if isinstance(formula, Symbol) or isinstance(formula, Predicate):
        text = str(formula)
    elif isinstance(formula, Not):
        text = "¬" + pretty_print(formula.args[0])
    else:
        temp = []
        for arg in formula.args:
            temp.append(pretty_print(arg))
        if isinstance(formula, And):
            text = " ∧ ".join(temp)
        elif isinstance(formula, Or):
            text = " ∨ ".join(temp)
        elif isinstance(formula, If):
            text = " → ".join(temp)
        elif isinstance(formula, Iff):
            text = " ↔ ".join(temp)
        else:
            raise TypeError("Invalid Formula Type: " + str(type(formula)))
        text = "(" + text + ")"
    return text.strip()


def is_connective(char):
    """
    Is the given character a logical connective (one of the pretty printed ones)
    :param char:
    :return:
    """
    return char in [u"¬", u"∧", u"∨", u"→", u"↔"]


def is_atomic(formula):
    """
    Is the given formula "Atomic" (contains no connectives), so Symbol or Predicate
    :param formula:
    :return:
    """
    return isinstance(formula, Symbol) or isinstance(formula, Predicate)


def is_binary_operator(formula):
    """
    Is the given formula a binary logical connective (and, or, if, iff)?
    :param formula:
    :return:
    """
    return isinstance(formula, And) or isinstance(formula, Or) \
        or isinstance(formula, If) or isinstance(formula, Iff)


def is_operator(formula):
    """
    Is the given formula a logical operator (binary connectives or not)
    :param formula:
    :return:
    """
    return is_binary_operator(formula) or isinstance(formula, Not)


def runner(formulas, display_connectives=True):
    """
    Generate the Truth Table for a given list of logical formulas in string form
    :param formulas:
    :param display_connectives:
    :return:
    """
    if isinstance(formulas, string_types):
        formulas = [formulas]

    if not isinstance(formulas, list):
        raise TypeError("Expected str or list, got " + str(type(formulas)))

    parsed_formulas = []
    for formula in formulas:
        formula = formula.strip()
        if len(formula) == 0:
            pass
        parsed_formulas.append(forseti.parser.parse(formula))
    return TruthTable(parsed_formulas, display_connectives=display_connectives)


class TruthTable(object):
    """
    Truth Table class
    """
    # pylint: disable=too-many-instance-attributes
    def __init__(self, formulas, display_connectives=True):
        """

        :param formulas:
        :return:
        """
        self.broken_formulas = []
        self.broken_evaluation = []
        self.evaluation = []
        self.connective_evaluation = []
        self.main_connective_index = []
        self.display_connectives = display_connectives
        self.symbols = []

        if not isinstance(formulas, list):
            raise TypeError("Invalid argument type, expected type list, "
                            "got " + str(type(formulas)))
        for formula in formulas:
            if not isinstance(formula, Formula):
                raise TypeError("Invalid argument in list, expected typed Formula, got " +
                                str(type(formula)))
        self.formulas = formulas
        self.break_apart_formulas()
        self.combinations = get_combinations(len(self.symbols))
        self.evaluate_table()

    def break_apart_formulas(self):
        """

        :return:
        """
        for formula in self.formulas:
            broken_formula = [formula]
            unbroken = [0]
            while len(unbroken) > 0:
                idx = unbroken.pop(0)
                if is_atomic(broken_formula[idx]):
                    if broken_formula[idx] not in self.symbols:
                        self.symbols.append(broken_formula[idx])
                else:
                    if isinstance(broken_formula[idx], Not):
                        for i in range(len(unbroken)):
                            if idx < unbroken[i]:
                                unbroken[i] += 1
                        broken_formula = broken_formula[:(idx + 1)] + \
                            [broken_formula[idx].args[0]] + broken_formula[(idx + 1):]
                        unbroken.append(len(broken_formula[:(idx + 1)]))
                    elif is_binary_operator(broken_formula[idx]):
                        for i in range(len(unbroken)):
                            if idx < unbroken[i]:
                                unbroken[i] += 2
                        broken_formula = broken_formula[:idx] + [broken_formula[idx].args[0]] + \
                            [broken_formula[idx]] + [broken_formula[idx].args[1]] + \
                            broken_formula[(idx + 1):]
                        unbroken.append(len(broken_formula[:idx]))
                        unbroken.append(len(broken_formula[:idx]) + 2)
            if len(broken_formula) > 0:
                self.broken_formulas.append(broken_formula)
        self.symbols.sort()

    def evaluate_table(self):
        """

        :return:
        """
        connective_index = [True] * len(self.formulas)
        for combination in self.combinations:
            broken_evaluation = []
            connective_evaluation = []
            evaluation = []
            for idx in range(len(self.broken_formulas)):
                broken_evaluation.append([])
                connective_evaluation.append([])
                for idx2 in range(len(self.broken_formulas[idx])):
                    broken = self.broken_formulas[idx][idx2]
                    temp = evaluate_formula(broken, self.symbols, combination)
                    broken_evaluation[-1].append(temp)
                    if is_operator(broken):
                        connective_evaluation[-1].append(temp)
                    if self.formulas[idx] == broken:
                        if connective_index[idx]:
                            if len(connective_evaluation[-1]) == 0:
                                self.main_connective_index.append([])
                            else:
                                self.main_connective_index.append([idx2, (len(connective_evaluation[-1])-1)])
                            connective_index[idx] = False
                        evaluation.append(temp)
            self.broken_evaluation.append(broken_evaluation)
            self.connective_evaluation.append(connective_evaluation)
            self.evaluation.append(evaluation)

    def generate_table(self):
        """

        :return:
        """
        pretty_formulas = [pretty_print(formula) for formula in self.formulas]
        table = " ".join([str(symbol) for symbol in self.symbols]) + " | "
        table += " ".join(pretty_formulas)
        table += "\n" + "-" * len(table) + "\n"

        for i in range(len(self.combinations)):
            table += " ".join(["T" if combination else "F" for combination in self.combinations[i]])
            table += " | "
            temps = []
            for j in range(len(pretty_formulas)):
                pretty = pretty_formulas[j]
                temp = ""
                cnt = 0
                for char in pretty:
                    if is_connective(char):
                        if self.main_connective_index[j][1] == cnt:
                            temp = temp[:-1]
                            temp += "-"
                        if self.display_connectives or self.main_connective_index[j][1] == cnt:
                            temp += "T" if self.connective_evaluation[i][j][cnt] else "F"
                        else:
                            temp += " "
                        cnt += 1
                    else:
                        temp += " "
                if len(temp.strip()) == 0:
                    temp = "T" if self.evaluation[i][j] else "F"
                temps.append(temp)
            table += " ".join(temps)
            table += "\n"
        return table

    def get_table_assessment(self):
        if len(self.formulas) == 1:
            temp = sum([i for j in range(len(self.combinations)) for i in self.evaluation[j]])
            if temp == len(self.combinations):
                return ["Sentence is a Tautology"]
            elif temp == 0:
                return ["Sentence is a Contradiction"]
            else:
                return ["Sentence is TT-Possible"]
        else:
            statements = []
            is_taut = True
            first_consequence = True
            last_consequence = True
            taut_consistent = False
            for i in range(len(self.combinations)):
                temp = self.evaluation[i][0]
                all_first_true = True
                all_last_true = True
                for j in range(len(self.evaluation[i])):
                    if self.evaluation[i][j] != temp:
                        is_taut = False
                    if all_first_true and j != 0:
                        all_first_true = self.evaluation[i][j]
                    if all_last_true and j != (len(self.evaluation[i])-1):
                        all_last_true = self.evaluation[i][j]

                if first_consequence and all_first_true:
                    first_consequence = self.evaluation[i][0]

                if last_consequence and all_last_true:
                    last_consequence = self.evaluation[i][-1]

                if not taut_consistent and all(self.evaluation[i]):
                    taut_consistent = True

            if is_taut:
                statements.append("Sentences are Tautologically Equivalent")

            if first_consequence:
                statements.append("First Sentence is Tautological Consequence of Others")

            if last_consequence:
                statements.append("Last Sentence is Tautological Consequence of Others")

            if taut_consistent:
                statements.append("Sentences are Tautologically Consistent")
        return statements


if __name__ == "__main__":
    PARSER = argparse.ArgumentParser(
        description="Generate Truth Table for a logical formula"
    )
    PARSER.add_argument(
        'formulas',
        metavar='formula',
        type=str,
        nargs="+",
        help='Logical formula'
    )
    PARSER.add_argument(
        '-c',
        action='store_const',
        const=False,
        default=True,
        help="Only show truth value of main connective"
    )
    PARSER_ARGS = PARSER.parse_args()
    TRUTH_TABLE = runner(PARSER_ARGS.formulas, display_connectives=PARSER_ARGS.c)
    print(TRUTH_TABLE.generate_table())
