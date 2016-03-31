import argparse
import os
import sys
import sympy as sp

def custom_strip(s):
    s = s.strip("\n")
    s = s.strip("\t")
    s = s.strip(" ")
    return s

def parse_rule_file(rule_file_name):
    with open(rule_file_name) as rule_file:
        ### A list of tuples of the form ([predicate_0, predicate_1, ...], conclusion)
        rule_list = []
        in_pred = 0
        ### Check if parsing a new rule or continuing to parse current rule
        ### Maintain variables that indicate whether we are looking at predicates 
        row = custom_strip(rule_file.next())
        while (row != "#endfile"):
            #print row
            if row == "#if":
                new_rule = ([], [])
                pred = 1
            elif row == "#then":
                pred = 0
            elif row == "#end":
                rule_list.append(new_rule)
            else:
                if pred == 1:
                    new_rule[0].append(row)
                else:
                    new_rule[1].append(row)

            row = custom_strip(rule_file.next())
        
        print "RULE LIST:"
        print rule_list
        return rule_list

def parse_fact_file(fact_file_name):
    with open(fact_file_name) as fact_file:
        fact_list = []
        for f in fact_file:
            f = custom_strip(f)
            fact_list.append(f)

        print "FACT LIST:"
        print fact_list
        return fact_list




def resolve(i, j):
    clause_i_literals = []
    clause_j_literals = []

    ### Determine if either clause i or j is simply a single symbol
    ### Then get the literals out of the clauses
    if type(i) == sp.Symbol:
        clause_i_literals.append(i)
    else:
        if len(i.args) == 1:
            clause_i_literals.append(sp.Not(i.args[0]))
        else:
            clause_i_literals = list(i.args)
    if type(j) == sp.Symbol:
        clause_j_literals.append(j)
    else:
        if len(j.args) == 1:
            clause_j_literals.append(sp.Not(j.args[0]))
        else:
            clause_j_literals = list(j.args)

    ### First makes a list of all unique literals
    ### Then prunes complementary literals
    new_literals = list(set(clause_i_literals + clause_j_literals))
    for x in new_literals:
        for y in new_literals:
            if x == ~y:
                new_literals.remove(x)
                new_literals.remove(y)
            else:
                pass

    ### Construct new clause from literals or the empty clause
    if len(new_literals) > 0:
        new_clause = new_literals[0]
        for l in new_literals[1:]:
            new_clause = new_clause | l

        return new_clause
    else:
        return None


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


def resolution(kb, q):
    s = kb & ~q
    clauses = list(s.args) # gets the clauses that are conjoined to make the CNF sentence
    new = []

    num_iter = 0

    while True:
        for i in clauses:
            for j in clauses:
                resolvent = resolve(i,j)

                #print "Resolvent:"
                #print resolvent

                if resolvent == None:
                    print i
                    print j
                    return True
                else:
                    new.append(resolvent)

        #print "New"
        #print new

        ### Check if new is a subset of clauses
        num_new_clauses = len(new)

        print "number of new clauses"
        print num_new_clauses

        for c in new:
            if c in clauses:
                num_new_clauses -= 1

        if num_new_clauses == 0:
            return False

        ### Update clauses
        clauses = list(set(clauses + new))

        num_iter += 1
        print num_iter


def TEST_resolution(kb, q):
    print resolution(kb,q)
    


def forward_chaining(kb, q):
    ### Extract all unique symbols from the kb
    clauses = list(kb.args)
    symbols = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            symbols.append(c)
        else:
            symbols_in_clause = c.args
            for s in symbols_in_clause:
                symbols.append(s)

    ### Construct agenda queue
    ### Initially the symbols known to be true in the kb
    agenda = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            agenda.append(c)

    ### Construct inferred table 
    ### Initially false for all symbols 
    inferred = dict((k,False) for k in symbols)

    ### Construct count table
    ### Where count[c] = number of symbols in c's premise
    counts = {}
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            counts[c] = 1 
            # Should this really be 1? Possibly 0? How many "premises" does the clause "A" have? 
            # How about the clause "~A"? 
        else:
            counts[c] = len(list(c.args)) - 1

    ### Auxiliary tables of premises and conclusions
    premises = {}
    conclusions = {}
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            premises[c] = None
            conclusions[c] = None
        else:
            symbols_in_clause = c.args
            premise_list = []
            for s in symbols_in_clause:
                if type(s) == sp.Not:
                    premise_list.append(sp.Not(s))
                else:
                    conclusion = s
            premises[c] = tuple(premise_list)
            conclusions[c] = conclusion
            
    ### Forward chaining algorithm
    while agenda:
        p = agenda.pop()
        if p == q:
            return True
        if inferred[p] == False:
            inferred[p] = True
            for c in clauses:
                if premises[c] and p in premises[c]:
                    counts[c] = counts[c] - 1
                if counts[c] == 0:
                    agenda.insert(0, conclusions[c])

    return False
    


def TEST_forward_chaining(kb, q):
    print forward_chaining(kb, q)


def main():
    #parser = argparse.ArgumentParser(description="An inference engine for poisonous mushroom identification.")
    #parser.add_argument("input", nargs=1, help="File describing mushroom or symptoms")
    #parser.add_argument("-m", "--mode", nargs=1, default=[], help="How to process your query.")
    #args = parser.parse_args()

    #parse_rule_file(sys.argv[1])
    #parse_fact_file(sys.argv[2])

    ### String representations of the knowledge base (KB)
    ### The KB consists of "facts" which are just literals (negated or not) 
    ### and "rules" which are implications.
    ### WARNING: 'Q' messes up something in SymPy. Don't use 'Q' as a literal anywhere. 
    kb_facts = ["A", "B", "~C"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P", "P >> Z"]
    kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L"]

    ### String representation of the query
    kb_query = ["Z"]

    
    ### First we convert the KB and the query into types that SymPy can work on
    kb_facts = [sp.sympify(f) for f in kb_facts]
    kb_rules = [sp.sympify(r) for r in kb_rules]
    kb_query = [sp.sympify(q) for q in kb_query] 

    ### For the resolution algorithm, the inputs are:
    ### KB - A CNF sentence representing the entire knowledge base
    ### Q  - A CNF sentence representing the query
    ### Note that the conjunction of KB and ~Q is itself a CNF sentence.
    kb = kb_facts + kb_rules # This just concatenates the lists
    kb_sentence  = kb[0]
    for k in kb[1:]: # At end of this loop, everything in the KB is conjoined
        kb_sentence = kb_sentence & k
    kb_cnf_sentence = sp.to_cnf(kb_sentence) # And now the sentence is in CNF

    print "Testing resolve:" 
    TEST_resolve()
    print "Testing resolution:"
    TEST_resolution(kb_cnf_sentence, kb_query[0])
    print "Testing forward chaining:"
    TEST_forward_chaining(kb_cnf_sentence, kb_query[0])


main()
