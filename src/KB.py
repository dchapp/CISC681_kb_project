import argparse
import os
import sys
import sympy as sp

from Inference import *
from TestCases import *

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
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P"]
    kb_rules = ["(A & B) >> L", "(A & P) >> L"]

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
    print "Testing backward chaining:"
    TEST_backward_chaining(kb_cnf_sentence, kb_query[0])


main()
