from collections import OrderedDict

"""
Removes all forms of whitespace from beginning and end of string s.
"""
def custom_strip(s):
    s = s.strip("\n")
    s = s.strip("\t")
    s = s.strip(" ")
    return s

"""
Replaces characters in strings that cause SymPy's sympify function to fail
or cause unwanted behavior when converting a string to a SymPy symbol.
"""
def custom_replace(s):
    s = s.replace("<", "less than")
    s = s.replace(">", "greater than")
    s = s.replace("=", "equals")
    s = s.replace("|", "or")
    s = s.replace("&", "and")
    s = s.replace("+", "plus")
    s = s.replace("*", "times")
    s = s.replace("/", "or")
    s = s.replace(".", "_point_")
    s = s.replace(",", "")
    s = s.replace(";", "")
    s = s.replace(":", "")
    s = s.replace("-", " ")
    s = s.replace(" ", "_")
    return s

"""
Determines if sublst is an ordered sublist of lst.
"""
def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))

"""
Removes duplicates from a list while maintaining the order of the remaining elements in the list.
Contrast with L = list(set(L)) which does not maintain order of elements. 
"""
def remove_duplicates_maintain_order(lst):
    return list(OrderedDict.fromkeys(lst))
