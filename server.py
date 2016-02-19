# -*- coding: utf-8 -*-

from __future__ import unicode_literals
from flask import Flask, Markup, render_template, request
from forseti.formula import Symbol, Predicate, Not, And, Or, If, Iff
from forseti.parser import parse
import truthtables
from truthtables import TRUE_STRING, FALSE_STRING

app = Flask(__name__)


def pretty_print(formula):
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
            raise TypeError("Invalid Formula Type: " + type(formula))
        text = "(" + text + ")"
    return Markup(text.strip())


@app.route("/")
def index_page():
    return render_template('index.html')


@app.route("/submit", methods=['POST'])
def generate_table():
    formulas = request.form.getlist('formula[]')
    i = 0
    while i < len(formulas):
        formulas[i] = str(formulas[i]).strip()
        if len(formulas[i]) == 0:
            del formulas[i]
            i -= 1
        i += 1
    form = Markup(render_template('form.html', formulas=formulas))
    pretty = []
    for i in range(len(formulas)):
        formulas[i] = str(formulas[i]).strip()
        try:
            pretty.append(pretty_print(parse(formulas[i])))
        except (SyntaxError, TypeError) as exception:
            return render_template('error.html', error=str(exception), form=form)

    symbols, values = truthtables.runner(formulas)
    rows = []
    for i in range(len(values)):
        rows.append([])
        for j in range(len(values[i][2])):
            temp = pretty[j]
            new_str = u""
            count = 0
            for k in range(len(temp)):
                if temp[k] not in ["¬", "∧", "∨", "→", "↔"]:
                    new_str += "&nbsp;"
                else:
                    new_str += values[i][2][j][1][count]
                    count += 1
            if new_str.replace("&nbsp;", "") == "":
                new_str = "<b><u>" + (TRUE_STRING if values[i][1][j] else FALSE_STRING) + "</u></b>"
            rows[-1].append(Markup(new_str))

    return render_template('table.html', formulas=pretty, symbols=symbols, combinations=values, rows=rows, form=form)

if __name__ == '__main__':
    app.debug = True
    app.run()
