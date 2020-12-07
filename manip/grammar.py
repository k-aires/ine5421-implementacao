# Helena Kunz Aires <07/11/2020>
# INE - UFSC

def verify_input(g_type,inp):
    ret = True

    inp = inp.split(" -> ")
    if len(inp) != 2:
        ret = False
    elif len(inp[0]) != 1:
        ret = False
    elif not inp[0].isalpha() or not inp[0].isupper():
        ret = False
    else:
        if g_type == 0:
            ret = _verify_regular(inp[1])
        elif g_type == 1:
            ret = _verify_context_free(inp[1])
        else:
            ret = False
    
    return ret

def _verify_regular(inp):
    ret = True
    inp = inp.split("|")

    if len(inp) == 0:
        ret = False
    else:
        for i in inp:
            if len(i) < 0 or len(i) > 2:
                ret = False
                break
            if not i[0].isalnum() or i[0].isupper():
                ret = False
                break
            if len(i) == 2:
                if not i[1].isalpha() or i[1].islower():
                    ret = False
                    break

    return ret

def _verify_context_free(inp):
    ret = True
    inp = inp.split("|")

    if len(inp) == 0:
        ret = False
    else:
        for i in inp:
            if len(i) < 0:
                ret = False
                break
            if not i[0].isalnum() and i[0] != "&":
                ret = False
                break

    return ret

def format_grammar(grammar):
    gram = {}

    for g in grammar:
        g = g.split(" -> ")
        if g[0] not in gram:
            gram[g[0]] = []
        g[1] = g[1].split("|")
        if len(g[1]) == 1:
            gram[g[0]].append[g[1][0]]
        else:
            for o in g[1]:
                gram[g[0]].append(o)

    return gram

def chomsky_normal_form(grammar):
    grammar = _empty_productions(grammar)
    grammar = _unitary_productions(grammar)
    grammar = _useless_symbols(grammar)

    gram = {}

    for head in grammar:
        if head not in gram:
            gram[head] = []
        body = grammar[head]
        for production in body:
            if len(production) == 1:
                if production.islower():
                    gram[head].append(production)
                else:
                    # TODO: adiciona em chomsky casos tipo A -> B
                    pass
            elif len(production) == 2:
                if production.isupper():
                    gram[head].append(production)
                else:
                    # TODO: adiciona em chomsky casos tipo A -> ab|aB|Ab
                    pass
            elif len(production) >= 3:
                # TODO: adiciona em chosky casos de produção com tamanho maior que 2
                pass

def _empty_productions(grammar):
    pass

def _unitary_productions(grammar):
    pass

def _useless_symbols(grammar):
    pass
