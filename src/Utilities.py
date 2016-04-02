def custom_strip(s):
    s = s.strip("\n")
    s = s.strip("\t")
    s = s.strip(" ")
    return s

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
    s = s.replace(" ", "_")
    return s

def contains_sublist(lst, sublst):
    n = len(sublst)
    return any((sublst == lst[i:i+n]) for i in xrange(len(lst)-n+1))
