#!/usr/bin/env python

import argparse
import os
import sys
import sympy as sp

from Inference import *
from Utilities import *
from MushroomFacts import *

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

def deduce_poison_type(kb, alg):
    poison_types = ["clitocybe muscarine", 
                    "orellanine", 
                    "gamma amanitin", 
                    "gyromitrin",
                    "inocybe muscarine",
                    "alpha amanitin",
                    "amatoxin",
                    "pleurocybellaziridine",
                    "trichothocene"]
    possible_poisons = []
    for p in poison_types:
        query_string = p + " poisoning"
        query = sp.sympify(custom_replace(query_string))
        if alg == "resolution":
            truth_value = resolution(kb, query)
        elif alg == "forward chaining":
            truth_value = forward_chaining(kb, query)
        elif alg == "backward chaining":
            truth_value = backward_chaining(kb, query)
        elif alg == "iterative backward chaining":
            truth_value = iterative_backward_chaining(kb, query)
        else:
            truth_value = False

        if truth_value == True:
            possible_poisons.append(query_string)

    return possible_poisons

def deduce_mushroom_genus(kb, alg):
    genuses = ["amanita", 
               "clitocybe",
               "cortinarius",
               "galerina",
               "gyromitra",
               "lepiota",
               "inocybe",
               "pholiotina",
               "pleurocybella",
               "podostroma",
               "troiga"]
    possible_genuses = []
    for g in genuses:
        query_string = "genus is " + g
        query = sp.sympify(custom_replace(query_string))
        if alg == "resolution":
            truth_value = resolution(kb, query)
        elif alg == "forward chaining":
            truth_value = forward_chaining(kb, query)
        elif alg == "backward chaining":
            truth_value = backward_chaining(kb, query)
        elif alg == "iterative backward chaining":
            truth_value = iterative_backward_chaining(kb, query)
        else:
            truth_value = False

        if truth_value == True:
            possible_genuses.append(query_string)

    return possible_genuses

def deduce_mushroom_species(kb, alg):
    species = ["amanita sphaerobulbosa",
               "amanita exitialis",
               "amanita arocheae",
               "amanita bisporigera",
               "amanita magnivelaris",
               "amanita ocreata",
               "amanita phalloides",
               "amanita smithiana",
               "amanita subjunquillea",
               "amanita verna",
               "amanita virosa",
               "clitocybe dealbata",
               "clitocybe rivulosa",
               "cortinarius gentillis",
               "cortinarius orellanus",
               "cortinarius rubellus",
               "cortinarius splendens",
               "galerina marginata",
               "galerina sulciceps",
               "gyromitra esculenta",
               "lepiota brunneoincarnata",
               "lepiota castanea",
               "lepiota helveola",
               "lepiota subincarnata",
               "inocybe erubescens",
               "pholiotina rugosa",
               "pleurocybella porrigens",
               "podostroma cornudamae",
               "troiga venenata"]
    possible_species = []
    for s in species:
        query_string = "species is " + s
        query = sp.sympify(custom_replace(query_string))
        if alg == "resolution":
            truth_value = resolution(kb, query)
        elif alg == "forward chaining":
            truth_value = forward_chaining(kb, query)
        elif alg == "backward chaining":
            truth_value = backward_chaining(kb, query)
        elif alg == "iterative backward chaining":
            truth_value = iterative_backward_chaining(kb, query)
        else:
            truth_value = False

        if truth_value == True:
            possible_species.append(query_string)

    return possible_species

def main():

    ### Determine whether to run the knowledge system in file or interactive mode
    ### to generate the knowledge base.
    rule_file_name = sys.argv[1]
    mode = raw_input("Interactive knowledge base construction mode? Enter 'yes' or 'no' ")
    ### Interactive mode
    if mode == "yes":
        kb = build_knowledge_base_interactive(rule_file_name)
    ### File mode
    elif mode == "no": 
        fact_file_name = raw_input("Enter fact file path: ")
        kb = build_knowledge_base(rule_file_name, fact_file_name)
    ### Reject invalid modes
    else:
        print "Invalid knowledge base construction mode. Exiting."
        exit()
       
    ### Determine whether to use a pre-determined query method--e.g. to generate all possible
    ### poisons that could be affecting the patient--or to prompt the user to enter whichever
    ### queries they choose. 
    query_mode = raw_input("Choose query mode: 'deduce poison type', 'deduce mushroom genus', 'deduce mushroom species', 'custom queries' ")
    if query_mode == "deduce posion type" or query_mode == "deduce mushroom genus" or query_mode == "deduce mushroom species":
        algorithm = raw_input("Choose inference algorithm: 'resolution', 'forward chaining', 'backward chaining', 'iterative backward chaining' ")
        if algorithm == "resolution" or algorithm == "forward chaining" or algorithm == "backward chaining" or algorithm == "iterative backward chaining":
            if query_mode == "deduce poison type":
                possible_poisons = deduce_poison_type(kb, algorithm)
                if possible_poisons:
                    for p in possible_poisons:
                        print p
            elif query_mode == "deduce mushroom genus":
                possible_genuses = deduce_mushroom_genus(kb, algorithm)
                if possible_genuses:
                    for g in possible_genuses:
                        print g
            elif query_mode == "deduce mushroom species":
                possible_species = deduce_mushroom_species(kb, algorithm)
                if possible_species:
                    for s in possible_species:
                        print s
        else:
            print "Invalid algorithm specified. Exiting."
            exit()

    elif query_mode == "custom queries":
        ### Prompt the user to enter queries
        print "You will be prompted to enter queries. If you wish to exit, type \"exit\"."
        while True:
            query = raw_input("Enter your query: ")
            if query == "exit":
                exit()
            else:
                query = sp.sympify(custom_replace(query))
                algorithm = raw_input("Enter which inference algorithm you want to use: ")
                if algorithm == "resolution":
                    truth_value = resolution(kb, query)
                    if truth_value == True:
                        print "Query is entailed by knowledge base."
                    else:
                        print "Query is not entailed by knowledge base."
                elif algorithm == "forward chaining":
                    truth_value = forward_chaining(kb, query)
                    if truth_value == True:
                        print "Query is entailed by knowledge base."
                    else:
                        print "Query is not entailed by knowledge base."
                elif algorithm == "backward chaining":
                    truth_value = backward_chaining(kb, query)
                    if truth_value == True:
                        print "Query is entailed by knowledge base."
                    else:
                        print "Query is not entailed by knowledge base."
                elif algorithm == "iterative backward chaining":
                    truth_value = iterative_backward_chaining(kb, query)
                    if truth_value == True:
                        print "Query is entailed by knowledge base."
                    else:
                        print "Query is not entailed by knowledge base."
                else:
                    print "Unsupported algorithm specified."

    else:
        print "Invalid query mode specified. Exiting now."
        exit()



main()
