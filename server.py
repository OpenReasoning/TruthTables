# -*- coding: utf-8 -*-

"""
Flask module for running the TruthTable module app
"""

from __future__ import unicode_literals
from flask import Flask, Markup, render_template, request
import truthtables

TRUE_STRING = "<span style='color: green;'>T</span>"
FALSE_STRING = "<span style='color: red;'>F</span>"

FLASK_APP = Flask(__name__)


@FLASK_APP.route("/")
def index_page():
    return render_template('index.html')


@FLASK_APP.route("/submit", methods=['POST'])
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

    try:
        table = truthtables.runner(formulas)
    except (SyntaxError, TypeError) as exception:
        return render_template('error.html', error=str(exception), form=form)

    pretty = [truthtables.pretty_print(formula) for formula in table.formulas]

    rows = []
    for i in range(len(table.combinations)):
        rows.append([])
        for j in range(len(table.formulas)):
            temp = pretty[j]
            new_str = u""
            count = 0
            for k in range(len(temp)):
                if not truthtables.is_connective(temp[k]):
                    new_str += "&nbsp;"
                else:
                    if table.main_connective_index[j][1] == count:
                        new_str += "<b><u>"
                    if table.connective_evaluation[i][j][count]:
                        new_str += TRUE_STRING
                    else:
                        new_str += FALSE_STRING
                    if table.main_connective_index[j][1] == count:
                        new_str += "</b></u>"
                    count += 1
            if len(new_str.replace("&nbsp;", "").strip()) == 0:
                new_str = "<b><u>" + (TRUE_STRING if table.evaluation[i][j] else
                                      FALSE_STRING) + "</u></b>"
            rows[-1].append(Markup(new_str))

    return render_template('table.html', formulas=pretty, table=table, rows=rows, form=form,
                           table_statements=table.get_table_assessment())

if __name__ == '__main__':
    FLASK_APP.debug = True
    FLASK_APP.run()
