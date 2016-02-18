# -*- coding: utf-8 -*-

from __future__ import print_function
import copy
import forseti.parser
from forseti.formula import Formula, Symbol, Predicate, Not, And, Or, If, Iff
import argparse


TRUE_STRING = "<span style='color: green;'>T</span>"
FALSE_STRING = "<span style='color: red;'>F</span>"


def get_symbols(formula):
    """

    :param formula:
    :type formula: Formula
    :return:
    """

    symbols = list()

    if isinstance(formula, Symbol) or isinstance(formula, Predicate):
        symbols.append(formula)
    else:
        for arg in formula.args:
            for i in get_symbols(arg):
                if i not in symbols:
                    symbols.append(i)
    return symbols


def break_formula(formula):
    broken = [copy.deepcopy(formula)]
    unbroken = [0]
    while len(unbroken) > 0:
        temp = unbroken.pop(0)
        if isinstance(broken[temp], Symbol) or isinstance(broken[temp], Predicate):
            # these cannot be broken apart anymore
            pass
        if isinstance(broken[temp], Not):
            broken = broken[:(temp+1)] + [copy.deepcopy(broken[temp].args[0])] + broken[(temp+1):]
            unbroken.append(len(broken[:(temp+1)]))
        elif isinstance(broken[temp], And) or isinstance(broken[temp], Or) or isinstance(broken[temp], If) or isinstance(broken[temp], Iff):
            for i in range(len(unbroken)):
                if temp < unbroken[i]:
                    unbroken[i] += 2
            broken = broken[:temp] + [copy.deepcopy(broken[temp].args[0])] + [broken[temp]] + [copy.deepcopy(broken[temp].args[1])] + broken[(temp+1):]
            unbroken.append(len(broken[:temp]))
            unbroken.append(len(broken[:temp])+2)

    return broken


def evaluate_argument(formula, symbols, combination):
    """

    :param formula:
    :param symbols:
    :param combination:
    :return:
    """
    formula = copy.deepcopy(formula)
    if isinstance(formula, Symbol) or isinstance(formula, Predicate):
        return combination[symbols.index(formula)]
    elif isinstance(formula, Not):
        return not evaluate_argument(formula.args[0], symbols, combination)
    else:
        args = formula.args
        for i in range(len(args)):
            args[i] = evaluate_argument(args[i], symbols, combination)
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
    for i in range(2**num):
        combinations.append(temp[::-1])
        for j in range(len(temp)):
            if temp[j] is True:
                temp[j] = False
                break
            else:
                temp[j] = True
    return combinations


def runner(formulas):
    """

    :param formulas:
    :type formulas: list|str
    :return:
    """
    if isinstance(formulas, list):
        symbols = []
        parsed_formulas = []
        broken_formulas = []
        for formula in formulas:
            if formula == "":
                continue
            parsed_formula = forseti.parser.parse(formula)
            parsed_formulas.append(parsed_formula)
            broken_formulas.append(break_formula(parsed_formula))
            for symbol in get_symbols(parsed_formula):
                if symbol not in symbols:
                    symbols.append(symbol)
        symbols.sort()
        combinations = get_combinations(len(symbols))
        evaluations = []
        symbol_evaluations = []
        for combination in combinations:
            eval_temp = []
            symbol_temp = []
            for i in range(len(broken_formulas)):
                formula = parsed_formulas[i]
                eval_temp.append(evaluate_argument(formula, symbols, combination))
                broken_formula = broken_formulas[i]
                temp = []
                temp3 = []
                for broken in broken_formula:
                    temp2 = evaluate_argument(broken, symbols, combination)
                    string = TRUE_STRING if temp2 else FALSE_STRING
                    if broken == formula:
                        string = "<b><u>" + string + "</u></b>"
                    if not (isinstance(broken, Symbol) or isinstance(broken, Predicate)):
                        temp3.append(string)
                    temp.append(temp2)
                symbol_temp.append([temp, temp3])
            evaluations.append(eval_temp)
            symbol_evaluations.append(symbol_temp)
        return symbols, [[combinations[i], evaluations[i], symbol_evaluations[i]] for i in range(len(combinations))]
    elif isinstance(formulas, str):
        formula = formulas
        parsed_formula = forseti.parser.parse(formula)
        symbols = sorted(get_symbols(parsed_formula))
        combinations = get_combinations(len(symbols))
        evaulations = []
        for combination in combinations:
            evaulations.append(evaluate_argument(parsed_formula, symbols, combination))
        return symbols, [[combinations[i], evaulations[i]] for i in range(len(combinations))]
    else:
        raise TypeError("Invalid argument type, it should be either str or list of strings")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Generate Truth Table for a logical formula")
    parser.add_argument('formulas', metavar='formula', type=str, nargs="+", help='Logical formula')
    args = parser.parse_args()
    symbols, combinations = runner(args.formulas)

    for i in range(len(combinations)):
        print(str(combinations[i][0]) + ": " + str(combinations[i][1]))
