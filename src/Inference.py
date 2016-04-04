import sympy as sp
from Utilities import *

"""
Computes the resolvent of a pair of clauses i and j.
Specifically, if a clause contains two literals which are each others' negations,
these literals are removed from the clause.
"""
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

def resolution(kb, q):
    s = kb & ~q
    clauses = list(s.args) # gets the clauses that are conjoined to make the CNF sentence
    new = []

    ### Check to make sure that q can actually be entailed
    ### Auxiliary tables of premises and conclusions
    conclusions = {}
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            conclusions[c] = None
        else:
            symbols_in_clause = c.args
            for s in symbols_in_clause:
                if type(s) != sp.Not:
                    conclusion = s
            conclusions[c] = conclusion

    ### Loop until we generate the empty clause as the resolvent of two clauses.
    ### If we do, that means the sentence s is unsatisfiable and entailment of q by kb is proven. 
    while True:
        for i in clauses:
            for j in clauses:
                resolvent = resolve(i,j)

                # print "Resolvent:"
                # print resolvent

                if resolvent == None:
                    # print i
                    # print j
                    return True
                else:
                    new.append(resolvent)

        ### Check if new is a subset of clauses
        num_new_clauses = len(new)
        for c in new:
            if c in clauses:
                num_new_clauses -= 1

        if num_new_clauses == 0:
            return False

        ### Update clauses
        clauses = list(set(clauses + new))

"""
Implementation of forward chaining inference. 
"""
def forward_chaining(kb, q):
    ### Extract all unique symbols from the kb
    clauses = list(kb.args)
    symbols = []

    ### Construct agenda queue
    ### Initially the symbols known to be true in the kb
    agenda = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            agenda.append(c)

    negation = False;
    ### check if query is a negation
    if type(q) == sp.Not and q.args[0] not in agenda:
        negation = True
        q = q.args[0]

    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            symbols.append(c)
        else:
            symbols_in_clause = c.args
            for s in symbols_in_clause:
                symbols.append(s)

    ### Construct inferred table 
    ### Initially false for all symbols 
    inferred = dict((k,False) for k in symbols)

    ### Construct count table
    ### Where count[c] = number of symbols in c's premise
    counts = {}
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            counts[c] = 1
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
    checked_agenda = []
    while agenda:

        p = agenda.pop()
        checked_agenda.append(p)

        if p == q:
            return True
        if inferred[p] == False:
            inferred[p] = True
            for c in clauses:
                if premises[c] and p in premises[c]:
                    counts[c] = counts[c] - 1
                if counts[c] == 0 and conclusions[c] not in agenda and conclusions[c] not in checked_agenda:
                    agenda.insert(0, conclusions[c])

    if negation == True:
        return True
    return False

"""
Worker function for recursive backward chaining implementation.
"""
def backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, q, negation):
    known_true_symbols = remove_duplicates_maintain_order(known_true_symbols)
    ### First check if query is a known true symbol
    if q in known_true_symbols:
        return True

    ### Otherwise, check if there is a conclusion matching q
    ### If not, fail immediately.
    else:
        if q not in conclusions.values():
            if negation == True:
                return True
            return False
        ### There is at least one implication with q as its conclusion
        ### Now we need to recurse on those implications' premises
        else:
            query_premise_sets = []
            for c in clauses:
                if conclusions[c] == q:
                    query_premise_sets.append(premises[c])
            ### Now loop through the premise sets to see if any of them are a subset of the KTS
            for qps in query_premise_sets:
                s1 = set(qps)
                s2 = set(known_true_symbols)
                if s1 < s2:
                    known_true_symbols.append(q)
                    return True
            candidate_conclusions = []
            for c in clauses:
                if conclusions[c] == q:
                    pending_premises = premises[c]
                    target = len(pending_premises)
                    for p in pending_premises:
                        ### Check if premise currently provable. If not, move on to next clause
                        if p not in conclusions.values() and p not in known_true_symbols:
                            break

                        t = backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, p, negation)
                        if t == True:
                            target = target - 1
                            known_true_symbols.append(p)

                    if target == 0:
                        return True
                    else:
                        continue
            
            if negation == True:
                return True
            return False

"""
Driver function for recursive backward chaining implementation.
"""
def backward_chaining(kb, q):
    clauses = list(kb.args)

    ### Construct list of symbols known to be true
    known_true_symbols = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            known_true_symbols.append(c)

    negation = False;
    ### check if query is a negation
    if type(q) == sp.Not and q.args[0] not in known_true_symbols:
        negation = True
        q = q.args[0]
    
    ### Construct tables of premises and conclusions keyed by clauses
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
    
    return backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, q, negation)

"""
Non-recursive implementation of backward chaining
"""
def iterative_backward_chaining(kb, q):
    clauses = list(kb.args)

    ### Construct list of symbols known to be true
    known_true_symbols = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            known_true_symbols.append(c)

    negation = False;
    ### check if query is a negation
    if type(q) == sp.Not and q.args[0] not in known_true_symbols:
        negation = True
        q = q.args[0]

    ### Construct tables of premises and conclusions keyed by clauses
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

    ### Check if query is a known true symbol
    if q in known_true_symbols:
        return True

    ### Check if query can possibly be entailed
    if q not in conclusions.values():
        if negation == True:
            return True
        return False


    ### Determine the clauses that can entail the query
    candidates = []
    for c in clauses:
        if conclusions[c] == q:
            candidates.append(c)

    ### Loop over the candidates
    tried_to_prove = [q]
    old_known_true_symbols = list(known_true_symbols)
    for c in candidates:
        things_to_prove = list(premises[c])
        under_consideration = []

        while things_to_prove:
            ttps1 = set(things_to_prove)
            ttps2 = set(tried_to_prove)
            if ttps1 < ttps2:
                if negation == True:
                    return True
                return False

            if old_known_true_symbols != known_true_symbols:
                for r in tried_to_prove:
                    if r in conclusions.values():
                        possible_premises = []
                        for c in clauses:
                            if conclusions[c] == r:
                                possible_premises.append(premises[c])
                        for pp in possible_premises:
                            s1 = set(known_true_symbols)
                            s2 = set(pp)
                            if s2 < s1:
                                known_true_symbols.append(r)
                                tried_to_prove.remove(r)

            t = things_to_prove.pop()

            ### If known to be true, do nothing
            if t in known_true_symbols:
                pass
            ### Can it proved by anything?
            elif t not in conclusions.values():
                tried_to_prove.append(t) 
                tried_to_prove = remove_duplicates_maintain_order(tried_to_prove)
                things_to_prove.insert(0,t)
                continue

            ### See if t can be proved using nothing but known true symbols. 
            ### If so, add it as a known true symbol. 
            ### If not, add it's premises to the stack.
            else:
                ### Did we already try to prove this and fail? 
                ### Has the known symbol true symbol list changed?
                if t in tried_to_prove and old_known_true_symbols == known_true_symbols:
                    break
                else:
                    for c in clauses:
                        if conclusions[c] == t:
                            things_that_prove_t = list(premises[c])

                            ### Check if t can be proved with nothing but known true symbols
                            if contains_sublist(known_true_symbols, things_that_prove_t):
                                old_known_true_symbols = list(known_true_symbols)
                                known_true_symbols.append(t)
                                if t in tried_to_prove:
                                    tried_to_prove.remove(t)
                                break
                            else:
                                things_to_prove = things_to_prove + things_that_prove_t
                                tried_to_prove.append(t)
                                tried_to_prove = remove_duplicates_maintain_order(tried_to_prove)
           
            things_to_prove = remove_duplicates_maintain_order(things_to_prove)
            
            if len(things_to_prove) == 0:
                return True

    if negation == True:
        return True
    return False


##################################################################################
################ End currently working inference algorithms ######################
##################################################################################


"""
Driver function for DPLL inference
"""
def dpll_satisfiable(kb, q):
    sentence = kb & ~q
    clauses = list(sentence.args)
    symbols = []
    for c in clauses:
        args = list(c.args)
        new_symbols = []
        for a in args:
            if type(a) == sp.Symbol:
                new_symbols.append(a)
            else:
                new_symbols.append(sp.Not(a))
        symbols = symbols + new_symbols
    symbols = list(set(symbols))
    model = {}
    return dpll(clauses, symbols, model)


"""
Worker function for DPLL inference
"""
def dpll(clauses, symbols, model):
    ### Determine if there is a clause that is false in the model
    target = len(clauses)
    for c in clauses:
        if clause_is_true_in_model(c, model) == "not in model":
            continue
        else:
            if clause_is_true_in_model(c, model):
                target -= 1
            else:
                return False
    if target == 0:
        return True

    ### Loop over symbols and recurse with modified models if pure symbol found
    #for s in symbols:
        #if is_pure_symbol(s, clauses

def clause_is_true_in_model(clause, model):
    if clause in model.keys():
        if model[clause] == True:
            return True
        else:
            return False
    else:
        return "not in model"

"""
Determines if the symbol appears with the same sign in all clauses.
"""
def is_pure_symbol(symbol, clauses):
    ### Get the instances of the symbol 

    #print symbol
    #print clauses

    instances = []
    for c in clauses:
        if type(c) == sp.Or:
            symbols_in_clause = list(c.args)
            for s in symbols_in_clause:
                if s == symbol or sp.Not(s) == symbol:
                    instances.append(s)
        else:
            if c == symbol or sp.Not(c) == symbol:
                instances.append(c)

    #print instances

    ### Determine if symbol appears with same sign everywhere
    instances = set(instances)

    #print instances

    if len(instances) == 1:
        return (True, symbol)
    else:
        return (False, symbol)

"""
Determines if the clause is a unit clause. 
A clause is a unit clause if it consists of a single symbol OR
if all but one symbol in the clause are already assigned false by the model.
"""
def is_unit_clause(clause, model):
    if type(clause) == sp.Symbol:
        return (True, clause)
    else:
        symbols_in_clause = list(clause.args)
        target = len(symbols_in_clause) - 1
        for s in symbols_in_clause:
            if s in model.keys():
                if model[s] == False:
                    target = target - 1
                else:
                    single_symbol = s
        if target == 0:
            return (True, single_symbol)
        else:
            return (False, 0)

