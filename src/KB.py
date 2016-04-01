import argparse
import os
import sys
import sympy as sp

from Inference import *
from TestCases import *
from Utilities import *


def parse_fact_file(fact_file_name):
    with open(fact_file_name) as fact_file:
        fact_list = []
        for f in fact_file:
            f = custom_strip(f)
            fact_list.append(f)

        print "FACT LIST:"
        print fact_list
        return fact_list


"""
Generates a list of SymPy implications representing rules in the knowledge base.
"""
def parse_rule_file(rule_file_name):

    ### Read in rules and separate their antecedents from their conclusions
    with open(rule_file_name) as rule_file:
        rule_list = []
        for line in rule_file:
            ### Ignore if line is a description or empty
            if line[0] == "#" or line == "\n":
                continue
            ### Otherwise add rule to list
            else:
                components = line.split("==>")
                premises = [custom_strip(x) for x in components[0].split("&")]
                conclusion = custom_strip(components[1])
                rule = (premises, conclusion)
                rule_list.append(rule)

    ### Format premises and conclusion properly and generate string
    rules = []
    for r in rule_list:
        premises = r[0]
        conclusion = r[1]
        premises = [custom_replace(x) for x in premises]
        conclusion = custom_replace(conclusion)
        rule_string = "("
        for p in premises:
            if p != premises[-1]:
                rule_string = rule_string + p + " & "
            else:
                rule_string = rule_string + p
        rule_string = rule_string + ") >> " + conclusion
        rules.append(rule_string)

    ### SymPy-fy
    rules = [sp.sympify(x) for x in rules]

    return rules



def run_inference_test_suite():
    ### String representations of the knowledge base (KB)
    ### The KB consists of "facts" which are just literals (negated or not) 
    ### and "rules" which are implications.
    ### WARNING: 'Q' messes up something in SymPy. Don't use 'Q' as a literal anywhere. 
    #kb_facts = ["A", "B", "~C"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P", "P >> Z"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L"]
    
    kb_facts = ["labored_breathing", "liver_failure", "~C"]
    kb_rules = ["(labored_breathing & liver_failure) >> L", "(labored_breathing & P) >> L", "(liver_failure & L) >> M", "(L & M) >> P", "P >> Z"]

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

    ### Print test results
    print "Testing resolve:" 
    TEST_resolve()
    print "Testing resolution:"
    TEST_resolution(kb_cnf_sentence, kb_query[0])
    print "Testing forward chaining:"
    TEST_forward_chaining(kb_cnf_sentence, kb_query[0])
    print "Testing backward chaining:"
    TEST_backward_chaining(kb_cnf_sentence, kb_query[0])


def main():
    #parser = argparse.ArgumentParser(description="An inference engine for poisonous mushroom identification.")
    #parser.add_argument("input", nargs=1, help="File describing mushroom or symptoms")
    #parser.add_argument("-m", "--mode", nargs=1, default=[], help="How to process your query.")
    #args = parser.parse_args()

    rules = parse_rule_file(sys.argv[1])
    run_inference_test_suite()

main()
