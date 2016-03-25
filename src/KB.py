import argparse
import os
import sys

from Rule import *

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

    parse_rule_file(sys.argv[1])
    parse_fact_file(sys.argv[2])

    #r = Rule(0,0)
    #print r.a
    #print r.c
    #print type(r)

    



main()
