import sympy as sp

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
        print "Number of new clauses: " + str(num_new_clauses)
        for c in new:
            if c in clauses:
                num_new_clauses -= 1

        if num_new_clauses == 0:
            return False

        ### Update clauses
        clauses = list(set(clauses + new))

        num_iter += 1
        print num_iter


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



def backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, q):
    ### First check if query is a known true symbol
    if q in known_true_symbols:
        return True
    ### Otherwise, check if there is a conclusion matching q
    ### If not, fail immediately.
    else:
        if q not in conclusions.values():
            return False
        ### There is at least one implication with q as its conclusion
        ### Now we need to recurse on those implications' premises
        else:
            candidate_conclusions = []
            for c in clauses:
                if conclusions[c] == q:
                    pending_premises = premises[c]
                    target = len(pending_premises)
                    for p in pending_premises:
                        t = backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, p)
                        if t == True:
                            target = target - 1

                    if target == 0:
                        return True
                    else:
                        return False



def backward_chaining(kb, q):
    clauses = list(kb.args)

    ### Construct list of symbols known to be true
    known_true_symbols = []
    for c in clauses:
        if type(c) == sp.Symbol or type(c) == sp.Not:
            known_true_symbols.append(c)


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

    return backward_chaining_helper(kb, clauses, known_true_symbols, premises, conclusions, q)

#    ### Backward chaining algorithm
#    candidates = []
#    for c in clauses:
#        if conclusions[c] == q:
#            ### Check if premises are in kb
#            candidate_premises = list(premises[c])
#
#            print "Candidate premises: " + str(candidate_premises)
#            print "Known true symbols: " + str(known_true_symbols)
#
#            m = len(candidate_premises)
#            n = 0
#
#            for p in candidate_premises:
#                if p in known_true_symbols:
#
#                    print p
#
#                    n += 1
#
#            if m == n:
#                return True
#            else:
#                candidates.append(c)
#
#    print "Candidates:"
#    print candidates
#
#    #num_premises = 0
#    for c in candidates:
#        print "Premises of " + str(c)
#        target = len(premises[c])
#        num_premises = 0
#        for p in premises[c]:
#            print p
#            result = backward_chaining(kb, p)
#            if result == True:
#                num_premises = num_premises + 1
#    
#        if num_premises == target:
#            return True
#    
#    return False



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
    model = []
    return dpll(clauses, symbols, model)


def dpll(clauses, symbols, model):
    ### Determine if there is a clause that is false in the model
    return False



