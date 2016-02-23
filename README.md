Truth Tables
============

[![Build Status](https://travis-ci.org/MasterOdin/TruthTables.svg?branch=master)](https://travis-ci.org/MasterOdin/TruthTables) [![Coverage Status](https://coveralls.io/repos/github/MasterOdin/TruthTables/badge.svg?branch=master)](https://coveralls.io/github/MasterOdin/TruthTables?branch=master)

This is a flask app (with a python module backing it) that can be used to generate Truth Trees for any number of given logical formulas.

![Flask App](https://raw.githubusercontent.com/MasterOdin/TruthTables/master/static/screenshot.png)

It uses a functional form for inputting logical formulas. This is the base identity for inputs:
```
A
not(A)
and(A, B)
or(A, B)
if(A, B)
iff(A, B)
```
where `A` and `B` can either be atomic statements or a functional operator. There is no use for generalized functions (everything is unary or binary functions).