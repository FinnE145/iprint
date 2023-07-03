# Copyright (C) 2022-2023 Finn Emmerson
# All Rights Reserved
# License: Proprietary

# ----------- iPrint ---------- #
iters = [dict, list, tuple, set]        # NOTE: 'dict' must be first, because it has special cases

def _length(i):
    return (sum([_length(k) + _length(v) + (3 if len(i.keys()) <= 1 else (2 if len(i.keys()) <= 0 else 4)) for k, v in i.items()]) + 1) if type(i) == dict else (sum([_length(x) + 2 for x in i]) if type(i) in iters else (len(i.__class__.__name__) + _length(i.__dict__) + len(i.__dict__.keys()) - 1 if hasattr(i, "__dict__") else len(str(i))))

def brackets(datatype, newline = False, indentAmount = 0):
    return [("[" if datatype == list else "(" if datatype == tuple else "{" if datatype in [set, dict] else "") + ("\n" if datatype in iters and newline else "") + (" " * indentAmount), ("\n" if datatype in iters and newline else "") + (" " * indentAmount) + ("]" if datatype == list else ")" if datatype == tuple else "}" if datatype in [set, dict] else "")]

def indent(indentLevel, indentDepth):
    return " " * (indentLevel * indentDepth)

def iformat(i, indentLevel = 0, indentDepth = 4, expansionThreshold = 10):
    il, id, et = indentLevel, indentDepth, expansionThreshold
    length = _length(i)
    if type(i) in iters:
        return (brackets(type(i), True if length > et else False, ((il + 1) * id) if length > et else False)[0]\
            + ((",\n" + indent(il + 1, id)) if length > et else (", ")).join(\
                    [f"{iformat(k, il + 1, id, et)}: {iformat(v, il + 1, id, et)}" for k, v in i.items()]\
                if type(i) == dict else\
                    [iformat(x, il + 1, id, et) for x in i])\
            + brackets(type(i), True if length > et else False, (il * id) if length > et else 0)[-1])
    else:
        if hasattr(i, "__dict__"):
            if "iformat" in dir(i):
                return i.iformat(il, id, et)
            else:
                return (f"{i.__class__.__name__}({', '.join([f'{k} = {iformat(v, il, id, et)}' for k, v in i.__dict__.items()])})")
        else:
            return str(i)

def iprint(*args, indentDepth = 4, expansionThreshold = 10, sep = " ", end = "\n", file = None, flush = False):
    print(*[iformat(x, 0, indentDepth, expansionThreshold = expansionThreshold) for x in args], sep = sep, end = end, file = file, flush = flush)