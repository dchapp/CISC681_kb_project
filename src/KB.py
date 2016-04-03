import argparse
import os
import sys
import sympy as sp

from Inference import *
from TestCases import *
from Utilities import *
from MushroomFacts import *

from DPLL import *

"""
Generate a list of SymPy symbols representing facts in the knowledge base
"""
def parse_fact_file(fact_file_name):
    
    ### Read in facts 
    with open(fact_file_name) as fact_file:
        fact_list = []
        for line in fact_file:
            if line[0] == "#" or line[0] == "\t" or line[0] == " " or line == "\n":
                continue
            else:
                fact_list.append(custom_strip(line))

    ### Format facts to generate Sympy-fiable strings
    facts = []
    for f in fact_list:
        facts.append(custom_replace(f))

    ### Transform to SymPy symbols
    facts = [sp.sympify(x) for x in facts]

    return facts

"""
Generates a list of SymPy implications representing rules in the knowledge base.
"""
def parse_rule_file(rule_file_name):

    ### Read in rules and separate their antecedents from their conclusions
    with open(rule_file_name) as rule_file:
        rule_list = []
        for line in rule_file:
            ### Ignore if line is a description, whitespace, or empty
            if line[0] == "#" or line[0] == "\t" or line[0] == " " or line == "\n":
                continue
            ### Otherwise add rule to list
            else:
                components = line.split("==>")
                premises = [custom_strip(x) for x in components[0].split("&")]
                conclusion = custom_strip(components[1])
                rule = (premises, conclusion)
                rule_list.append(rule)

    ### Format premises and conclusion to generate SymPy-fiable string
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

    ### Transform to SymPy implications
    rules = [sp.sympify(x) for x in rules]

    return rules


"""
Constructs a knowledge base from a file of rules and a file of facts.
The knowledge base is constructed as a CNF sentence suitable for use with the inference algorithms. 
"""
def build_knowledge_base(rule_file_name, fact_file_name):
    rules = parse_rule_file(rule_file_name)
    facts = parse_fact_file(fact_file_name)
    kb    = rules + facts 
    kb_sentence = kb[0]
    for k in kb[1:]:
        kb_sentence = kb_sentence & k

    kb_cnf_sentence = sp.to_cnf(kb_sentence)
    return kb_cnf_sentence


"""
Constructs a knowledge base from a file of rules and uses user input to establish a list of facts.
The knowledge base is constructed as a CNF sentence suitable for use with the inference algorithms. 
"""
def build_knowledge_base_interactive(rule_file_name):
    rules = parse_rule_file(rule_file_name)
    (mushroom_properties, patient_properties) = define_properties()
    fact_list = []
    ### First iterate through list of mushroom properties and get user responses
    print "Please answer the following questions about the mushroom the patient ingested."
    print "If you do not know the answer, please enter \"?\""
    for p in mushroom_properties:
        if p == "stem has ring" or p == "stem has volva":
            response = raw_input("Does the mushroom's " + p.replace("has", "have a") + "? ")
            if response == "yes":
                fact_list.append(p)
            else:
                continue
        else:
            response = raw_input("What is the mushroom's " + p + "? ")
            if response == "?" or response == "\n":
                continue
            else:
                fact = p + " is " + response
                fact_list.append(fact)

    ### Next iterate through list of patient properties and get user responses
    print "Please answer the following questions about the patient."
    for p in patient_properties:
        response = raw_input("Does the patient have " + p + "? ")
        if response == "yes":
            fact_list.append(p)
        else:
            continue

    ### Format facts for conversion to SymPy symbols
    facts = []
    for f in fact_list:
        facts.append(custom_replace(f))

    ### Convert facts to SymPy symbols
    facts = [sp.sympify(x) for x in facts]

    ### Assemble KB
    kb = rules + facts
    kb_sentence = kb[0]
    for k in kb[1:]:
        kb_sentence = kb_sentence & k

    kb_cnf_sentence = sp.to_cnf(kb_sentence)
    return kb_cnf_sentence





def run_inference_test_suite(query):
    ### String representations of the knowledge base (KB)
    ### The KB consists of "facts" which are just literals (negated or not) 
    ### and "rules" which are implications.
    ### WARNING: 'Q' messes up something in SymPy. Don't use 'Q' as a literal anywhere. 
    #kb_facts = ["A", "B", "~C"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P", "P >> Z"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L", "(B & L) >> M", "(L & M) >> P"]
    #kb_rules = ["(A & B) >> L", "(A & P) >> L"]
    
    #kb_facts = ["labored_breathing", "liver_failure", "~C"]
    #kb_rules = ["(labored_breathing & liver_failure) >> L", "(labored_breathing & P) >> L", "(liver_failure & L) >> M", "(L & M) >> P", "P >> Z"]

    ### String representation of the query
    #kb_query = ["Z"]

    ### First we convert the KB and the query into types that SymPy can work on
   # kb_facts = [sp.sympify(f) for f in kb_facts]
   # kb_rules = [sp.sympify(r) for r in kb_rules]
   # kb_query = [sp.sympify(q) for q in kb_query] 

   # ### For the resolution algorithm, the inputs are:
   # ### KB - A CNF sentence representing the entire knowledge base
   # ### Q  - A CNF sentence representing the query
   # ### Note that the conjunction of KB and ~Q is itself a CNF sentence.
   # kb = kb_facts + kb_rules # This just concatenates the lists
   # kb_sentence  = kb[0]
   # for k in kb[1:]: # At end of this loop, everything in the KB is conjoined
   #     kb_sentence = kb_sentence & k
   # kb_cnf_sentence = sp.to_cnf(kb_sentence) # And now the sentence is in CNF

    kb = build_knowledge_base("../test/rules1.txt", "../test/facts1.txt")
    q  = sp.sympify(custom_replace(query))

    ### Print test results
    #print "Testing resolve:" 
    #TEST_resolve()
    print "Testing forward chaining:"
    TEST_forward_chaining(kb, q)
    print "Testing recursive backward chaining:"
    TEST_backward_chaining(kb, q)
    print "Testing iterative backward chaining:"
    print iterative_backward_chaining(kb, q)

    #print "Testing resolution"
    #print resolution(kb, q)


    print "Testing DPLL"
    print dpll_satisfiable((kb & ~q))
    
    """
    print parse_fact_file("../test/facts1.txt")
    print parse_rule_file("../test/rules1.txt")
    print "KB"
    print kb
    print "SENTENCE"
    print (kb & ~q).args
    """

def main():
    #parser = argparse.ArgumentParser(description="An inference engine for poisonous mushroom identification.")
    #parser.add_argument("rule file", nargs=1, help="File listing rules.")
    #parser.add_argument("-m", "--mode", nargs=1, default=0, help="Determines whether to establish facts with a file (-m 0) or interactively (-m 1).")
    #args = parser.parse_args()

    ### Determine whether to run the knowledge system in file or interactive mode
    ### and generate the knowledge base.

#    rules = parse_rule_file(rule_file_name)
#    facts_from_file = parse_fact_file(fact_file_name)
#    print "RULES:"
#    print rules
#    print "FACTS:"
#    print facts_from_file
#
#    print "TESTING KB BUILDER"
#    kb_from_file = build_knowledge_base(rule_file_name, fact_file_name)
#    print kb_from_file
#
#    print "TESTING INTERACTIVE KB BUILDER"
#    kb_interactive = build_knowledge_base_interactive(rule_file_name)
#    print kb_interactive
#
    print "TESTING INFERENCE ALGORITHMS"
    run_inference_test_suite(sys.argv[1])

main()
