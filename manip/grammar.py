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
    initial = grammar[0].split(" -> ")[0]
    alphabet = set()
    productions = {}

    for g in grammar:
        g = g.split(" -> ")
        if g[0] not in productions:
            productions[g[0]] = []
        g[1] = g[1].split("|")
        for body in g[1]:
            for char in body:
                if not char.isupper():
                    alphabet.add(char)
            productions[g[0]].append(body)

    gram = {}
    gram["initial"] = initial
    gram["aplhabet"] = alphabet
    gram["productions"] = productions

    return gram

def chomsky_normal_form(grammar):
    grammar = _empty_productions(grammar)
    grammar = _unitary_productions(grammar)
    grammar = _useless_symbols(grammar)

    productions = {}

    for head,body in grammar["productions"]:
        if head not in productions:
            productions[head] = []
        for production in body:
            if len(production) == 1:
                if production.islower():
                    productions[head].append(production)
            elif len(production) == 2:
                if production.isupper():
                    productions[head].append(production)
                else:
                    # TODO: adiciona em chomsky casos tipo A -> ab|aB|Ab
                    pass
            elif len(production) >= 3:
                # TODO: adiciona em chosky casos de produção com tamanho maior que 2
                pass

def _empty_productions(grammar):
    if "&" in grammar["alphabet"]:
        return
    
    epsilon = {"&"}
    while True:
        new = {}
        for head,body in grammar["productions"]:
            if head in epsilon:
                continue
            
            for prod in body:
                all_epsilon = True
                for symbol in prod:
                    if symbol not in epsilon:
                        all_epsilon = False
                        break
                if all_epsilon:
                    new.add(head)
                    break
        
        if len(new) == 0:
            break
        epsilon = epsilon.union(new)
    
    productions = {}
    for head,body in grammar["productions"]:
        for prod in body:
            if prod == "&":
                continue
            if head not in productions:
                productions[head] = []
            productions[head].append(prod)
            new = ""
            for symbol in prod:
                if symbol not in epsilon:
                    new += symbol
            if new != prod and new != "":
                productions[head].append(new)
    
    if grammar["initial"] in epsilon:
        initial = grammar["initial"]+"\'"
        productions[initial] = [grammar["initial"],"&"]
        grammar["initial"] = initial
    else:
        grammar["alphabet"].remove("&")
    
    grammar["productions"] = productions

def _unitary_productions(grammar):
    # Expects grammar to be free of empty productions
    reach = {}
    

def _useless_symbols(grammar):
    grammar = _nonproductive_symbols(grammar)
    grammar = _unreachable_symbols(grammar)

def _nonproductive_symbols(grammar):
    productive = set(grammar["alphabet"])
    productive.add("&")
    
    while True:
        new = set()
        for head,body in grammar["productions"]:
            produces = True
            for production in body:
                produces = True
                for symbol in production:
                    if symbol not in productive:
                        produces = False
                        break
                if produces:
                    break
            if produces and head not in productive:
                new.add(head)
        
        if len(new) == 0:
            break
        productive = productive.union(new)

    productions = {}
    for head,body in grammar["productions"]:
        if head not in productive:
            continue
        for prod in body:
            produces = True
            for symbol in prod:
                if symbol not in productive:
                    produces = False
                    break
            if not produces:
                continue
            if head not in productions:
                productions[head] = []
            productions[head].append(prod)
    
    grammar["productions"] = productions

def _unreachable_symbols(grammar):
    alphabet = set()
    reachable = set()
    new = {grammar["initial"]}

    while True:
        reachable = reachable.union(new)
        aux = set()
        for reach in new:
            productions = grammar["productions"][reach]
            for prod in productions:
                for symbol in prod:
                    if not symbol.isupper():
                        alphabet.add(symbol)
                    elif symbol in grammar["productions"]:
                        if symbol not in reachable:
                            aux.add(symbol)
        new = aux.copy()
        if len(new) == 0:
            break
    
    productions = {}
    for head,body in grammar["productions"]:
        if head in reachable:
            productions[head] = body
    
    grammar["productions"] = productions
