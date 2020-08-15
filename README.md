Truth Tables
============

[![Test](https://github.com/OpenReasoning/TruthTables/workflows/Test/badge.svg?branch=master&event=push)](https://github.com/OpenReasoning/TruthTables/actions?query=event%3Apush+workflow%3ATest)
[![codecov](https://codecov.io/gh/OpenReasoning/TruthTables/branch/master/graph/badge.svg)](https://codecov.io/gh/OpenReasoning/TruthTables)

This is a flask app (with a python module backing it) that can be used to generate Truth Tables for any number of given logical formulas.

![Flask App](https://raw.githubusercontent.com/MasterOdin/TruthTables/master/static/screenshot.png)

It uses a functional format for inputting logical formulas. This is the base identity for inputs:
```
A
not(A)
and(A, B)
or(A, B)
if(A, B)
iff(A, B)
```
where `A` and `B` can either be atomic statements or a functional operator. All operators are either unary (not) or binary (and, or, if, iff) and there is no support for a generalized notation. This means that ```and(A, B, C)``` will thrown an error.
