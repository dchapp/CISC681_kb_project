import sympy as sp
from Inference import *

def TEST_resolve():
    A = sp.sympify("A")
    B = sp.sympify("B")
    C = sp.sympify("C")

    ### Test a case that produces the empty clause
    clause_i = A
    clause_j = sp.Not(A)
    print resolve(clause_i, clause_j)

    ### Test a case that produces a non-empty clause
    clause_i = A
    clause_j = sp.Or(C, sp.Not(A), sp.Not(B))
    print resolve(clause_i, clause_j)

    ### Test a case that produces a non-empty clause with a repeated literal
    clause_i = A
    clause_j = sp.Or(C, sp.Not(A), sp.Not(B), A)
    print resolve(clause_i, clause_j)

def TEST_resolution(kb, q):
    print resolution(kb,q)

def TEST_forward_chaining(kb, q):
    print forward_chaining(kb, q)

def TEST_backward_chaining(kb, q):
    print backward_chaining(kb, q)


