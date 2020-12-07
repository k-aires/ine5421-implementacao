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
                if char.islower():
                    alphabet.add(char)
            productions[g[0]].append(body)

    gram = {}
    gram["initial"] = initial
    gram["alphabet"] = list(alphabet)
    gram["productions"] = productions

    return gram

def chomsky_normal_form(grammar):
    # New states, if exist, use #+(number)
    grammar = _empty_productions(grammar)
    grammar = _unitary_productions(grammar)
    grammar = _useless_symbols(grammar)

    productions = {}

    for head in grammar["productions"]:
        body = grammar["productions"][head]
        if head not in productions:
            productions[head] = []
        for production in body:
            length = _get_word_size(production)
            if length == 1:
                    productions[head].append(production)
            elif length == 2:
                if production.isupper():
                    productions[head].append(production)
                else:
                    first,position = _get_next_symbol(0,production)
                    second,position = _get_next_symbol(position,production)
                    new = ""
                    if first.islower():
                        state = "{"+first.capitalize()+"#0}"
                        if state not in productions:
                            productions[state] = [first]
                        new += state
                    else:
                        new += first
                    if second.islower():
                        state = "{"+second.capitalize()+"#0}"
                        if state not in productions:
                            productions[state] = [second]
                        new += state
                    else:
                        new += second
                    productions[head].append(new)
            elif length >= 3:
                new = _break_productions(head,production)
                for newh,newb in new:
                    if newh not in productions:
                        productions[newh] = []
                    productions[newh] += newb
    
    grammar["productions"] = productions
    return grammar

def _break_productions(head,production):
    productions = {}

    symbol,position = _get_next_symbol(0,production)
    next_state = "{"+head+"#1}"
    productions[head].append(symbol+next_state)
    for i in range(1,length-3):
        symbol,position = _get_next_symbol(position,production)
        new = "{"+head+"#"+i+1+"}"
        productions[next_state] = symbol+new
        next_state = new
    last,position = _get_next_symbol(position,production)
    symbol,position = _get_next_symbol(position,production)
    productions[next_state] = last+symbol

    return productions

def _empty_productions(grammar):
    # New state, if exists, uses '
    if "&" in grammar["alphabet"]:
        return
    
    epsilon = {"&"}
    while True:
        new = set()
        for head in grammar["productions"]:
            body = grammar["productions"][head]
            if head in epsilon:
                continue
            
            for prod in body:
                all_epsilon = True
                for position in range(0,len(prod)):
                    symbol,position = _get_next_symbol(position,prod)
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
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        for prod in body:
            if prod == "&":
                continue
            if head not in productions:
                productions[head] = []
            productions[head].append(prod)
            new = ""
            for position in range(0,len(prod)):
                symbol,position = _get_next_symbol(position,prod)
                if symbol not in epsilon:
                    new += symbol
            if new != prod and new != "":
                productions[head].append(new)
    
    if grammar["initial"] in epsilon:
        initial = "{"+grammar["initial"]+"\'"+"}"
        productions[initial] = [grammar["initial"],"&"]
        grammar["initial"] = initial
    elif "&" in grammar["alphabet"]:
        grammar["alphabet"].remove("&")
    
    grammar["productions"] = productions
    return grammar

def _unitary_productions(grammar):
    # Expects grammar to be free of empty productions
    reach = {}
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        for prod in body:
            if prod in grammar["productions"]:
                if head not in reach:
                    reach[head] = set()
                reach[head].add(prod)
    while True:
        new = {}
        for head in reach:
            body = grammar["productions"][head]
            for prod in body:
                if prod in reach:
                    if head not in new:
                        new[head] = []
                    new[head] = reach[prod]
                    if head in new[head]:
                        new.remove(head)
        
        for head in new:
            body = grammar["productions"][head]
            reach[head] = reach[head].union(new[head])

        if len(new) == 0:
            break
    
    productions = {}
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        productions[head] = body

        if head not in reach:
            continue
        
        for prod in reach[head]:
            productions[head] += grammar["productions"][prod]
        
        for prod in reach[head]:
            productions[head].remove(prod)
    
    grammar["productions"] = productions
    return grammar

def _useless_symbols(grammar):
    grammar = _nonproductive_symbols(grammar)
    grammar = _unreachable_symbols(grammar)
    return grammar

def _nonproductive_symbols(grammar):
    productive = set(grammar["alphabet"])
    productive.add("&")
    
    while True:
        new = set()
        for head in grammar["productions"]:
            body = grammar["productions"][head]
            produces = True
            for prod in body:
                produces = True
                for position in range(0,len(prod)):
                    symbol,position = _get_next_symbol(position,prod)
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
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        if head not in productive:
            continue
        for prod in body:
            produces = True
            for position in range(0,len(prod)):
                symbol,position = _get_next_symbol(position,prod)
                if symbol not in productive:
                    produces = False
                    break
            if not produces:
                continue
            if head not in productions:
                productions[head] = []
            productions[head].append(prod)
    
    grammar["productions"] = productions
    return grammar

def _unreachable_symbols(grammar):
    alphabet = set()
    reachable = set()
    new = {grammar["initial"]}

    while True:
        reachable = reachable.union(new)
        aux = set()
        for reach in new:
            production = grammar["productions"][reach]
            for prod in production:
                for position in range(0,len(prod)):
                    symbol,position = _get_next_symbol(position,prod)
                    if not symbol.isupper():
                        alphabet.add(symbol)
                    elif symbol in grammar["productions"]:
                        if symbol not in reachable:
                            aux.add(symbol)
        new = aux.copy()
        if len(new) == 0:
            break
    
    productions = {}
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        if head in reachable:
            productions[head] = body
    
    grammar["alphabet"] = list(alphabet)
    grammar["productions"] = productions
    return grammar

def factorization(grammar):
    pass

def left_recursion(grammar):
    # New states, if any, use "
    grammar = _indirect_left_recursion(grammar)
    grammar = _direct_left_recursion(grammar)
    return grammar

def _direct_left_recursion(grammar):
    have_recursion = set()
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        for prod in body:
            first,position = _get_next_symbol(0,prod)
            if first == head:
                have_recursion.add(head)
                break
    
    if len(have_recursion) > 0 and "&" not in grammar["alphabet"]:
        grammar["alphabet"].append("&")

    productions = {}
    for head in grammar["productions"]:
        body = grammar["productions"][head]
        if head not in have_recursion:
            productions[head] = body
            continue
        productions[head] = []
        new = "{"+head+"\"}"
        productions[new] = ["&"]
        for prod in body:
            first,position = _get_next_symbol(0,prod)
            if first == head:
                productions[new].append(prod+new)
            else:
                productions[head].append(prod+new)
    
    grammar["productions"] = productions
    return grammar

def _indirect_left_recursion(grammar):
    nonterminals = []
    for head in grammar["productions"]:
        nonterminals.append(head)

    productions = {}
    productions[nonterminals[0]] = grammar["productions"][nonterminals[0]]
    for i in range(0,len(nonterminals)):
        if nonterminals[i] not in productions:
            productions[nonterminals[i]] = []
        for j in range(0,i):
            for prod in grammar["productions"][nonterminals[i]]:
                first,position = _get_next_symbol(0,prod)
                if first != nonterminals[j]:
                    productions[nonterminals[i]].append(prod)
                    continue
                word = prod.lstrip(first)
                for complement in grammar["productions"][nonterminals[j]]:
                    productions[nonterminals[i]].append(complement+word)
    
    grammar["productions"] = productions
    return grammar

def _get_next_symbol(position,word):
    if position >= len(word):
        return ["",position]
    
    symbol = ""
    next_position = position+1
    if word[position] == "{":
        symbol += word[position]
        while True:
            if next_position == len(word):
                break
            symbol += word[next_position]
            if word[next_position] == "}":
                next_position += 1
                break
            next_position += 1
    else:
        symbol = word[position]
    
    return [symbol,next_position]

def _get_word_size(word):
    length = 0
    for i in range(0,len(word)):
        symbol,i = _get_next_symbol(i,word)
        length += 1
    
    return length
