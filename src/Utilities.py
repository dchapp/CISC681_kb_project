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
    s = s.repalce(";", "")
    s = s.replace(":", "")
    s = s.replace(" ", "_")
    return s
