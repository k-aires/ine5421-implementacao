from enum import Enum
from treelib import Node, Tree

class Group(Enum):
    DIGIT = "0|1|2|3|4|5|6|7|8|9"
    L_ALPHA = "a|b|c|d|e|f|g|h|i|j|k|l|m|n|o|p|q|r|s|t|u|v|x|w|y|z"
    U_ALPHA = "A|B|C|D|E|F|G|H|I|J|K|L|M|N|O|P|Q|R|S|T|U|V|X|W|Y|Z"
    I_ALPHA = L_ALPHA + "|" + U_ALPHA
    L_ALNUM = L_ALPHA + "|" + DIGIT
    U_ALNUM = U_ALPHA + "|" + DIGIT
    I_ALNUM = I_ALPHA + "|" + DIGIT

class Symbols(Enum):
    OPERATIONS = ["|","*","?","+"]
    GROUP = ["(",")"]
    
def verify_input(inp):
    ret = True
    split_inp = inp.partition(": ")
    if split_inp[1] == "":
        ret = False
    elif not split_inp[0].isalnum():
        ret = False
    elif not _verify_pattern(split_inp[2]):
        ret = False
   
    return ret

def _verify_pattern(pattern):
    match = True
    char_stack = [""]
    char_before = ""
    group_test = False
    for char in pattern:
        if group_test: # Entra em verificação de grupo
            if char == "]": # Termina grupo
                if char_stack[-1] != "[":
                    match = False
                    break
                char_stack.pop()
                group_test = False
            elif char == "a" or char == "A" or char == "0": # Verifica início do grupo
                if char_before == "-":
                    match = False
                    break
                char_stack.append(char)
            elif char == "z": # Verifica final do grupo [a-z]
                if char_before != "-" or char_stack[-1] != "a":
                    match = False
                    break
                char_stack.pop()
                if char_stack[-1] != "[": # Não pode ter grupo dentro de grupo
                    match = False
                    break
            elif char == "Z": # Verifica final do grupo [A-Z]
                if char_before != "-" or char_stack[-1] != "A":
                    match = False
                    break
                char_stack.pop()
                if char_stack[-1] != "[":
                    match = False
                    break
            elif char == "9": # Verifica final do grupo [0-9]
                if char_before != "-" or char_stack[-1] != "0":
                    match = False
                    break
                char_stack.pop()
                if char_stack[-1] != "[":
                    match = False
                    break
            elif char != "-": # Não aceita símbolos além de - e os verificados acima
                match = False
                break
        else:
            if char_before == "\\": # Indica que o char atual não é para ser tratado como símbolo
                continue
            if char == "|": # Verifica se ou (|) possui construção válida anterior
                if char_before == "" or char_before == "(" or char_before == "[":
                    match = False
                    break
            elif char_before == "|": # Verifica se ou (|) possui construção válida posterior
                if not char.isalnum():
                    match = False
                    break
            elif char == "-": # Não aceita - se não está em grupo
                match = False
                break
            elif char == "[": # Adiciona na pilha e começa verificação de grupo
                char_stack.append(char)
                group_test = True
            elif char == "(": # Adiciona na pilha
                char_stack.append(char)
            elif char == "]": # Não aceita ] se não está em grupo
                match = False
                break
            elif char == ")": # Verifica se existe ( correspondente e tira da pilha
                if char_stack[-1] != "(":
                    match = False
                    break
                char_stack.pop()
            elif char == "*" or char == "+" or char == "?": # Verifica se operações possuem construção válida
                if char_before != ")" and char_before != "]" and not char_before.isalnum():
                    match = False
                    break
                        
        char_before = char
    
    if match: # Verifica o final da expressão, se possui escopo aberto, etc
        if char_stack[-1] != "":
            match = False
        elif char_before == "|":
            match = False
    
    return match

def format_expression(expression):
    exp = {}
    for e in expression:
        e = e.split(": ")
        exp[e[0]] = e[1]
    return exp

def afd_conversion(expression):
    exp = _condense_expression(expression)
    tree = _sytanx_tree(exp)
    automata = {}
    return automata

def _nullable(tree):
    ret = True
    return ret

def _first_pos(tree):
    ret = set()
    return ret

def _last_pos(tree):
    ret = set()
    return ret

def _sytanx_tree(expression):
    trees = []
    tree_count = -1
    symbol_count = 1
    tree_stack = []
    last = ""
    for symbol in expression:
        if last != "":
            if symbol in Symbols.OPERATIONS.value:
                if symbol == "|":
                    tree_stack.append(last)
                else:
                    _add_to_syntax_tree(symbol,last,symbol_count,trees,tree_count)
            else:
                _add_to_syntax_tree(".",last,symbol_count,trees,tree_count)
            if last == ")":
                tree_count -= 1
            last = ""
            symbol_count += 1
        elif symbol == "|":
            tree_stack.append("|")

        if symbol in Symbols.GROUP.value:
            if symbol == "(":
                tree_stack.append(symbol)
                trees.append(Tree())
                tree_count += 1
            else:
                if tree_stack[-1] != "(":
                    pass
                tree_stack.pop()
                last = symbol
        elif symbol not in Symbols.OPERATIONS.value:
            if tree_stack and tree_stack[-1] == "|":
                _add_to_syntax_tree(tree_stack.pop(),symbol,symbol_count,trees,tree_count)
            elif (tree_stack[-1] not in Symbols.OPERATIONS.value
                and tree_stack[-1] not in Symbols.GROUP.value):
                _start_or_chain_syntax_tree(tree_stack.pop(),symbol,symbol_count,trees,tree_count)
            else:
                last = symbol

    trees[0].show(idhidden=False)
    return trees[0]

def _add_to_syntax_tree(operand,symbol,symbol_count,trees,tree_count):
    symbol_tree = Tree()
    symbol_tree.create_node(symbol,str(symbol_count))
    if symbol == ")":
        tree = trees[tree_count]
        if operand == ".":
            symbol_tree = _copy_tree(tree)
        else:
            symbol_tree = Tree()
            root_id = operand+str(symbol_count)
            symbol_tree.create_node(operand,root_id)
            symbol_tree.paste(root_id,_copy_tree(tree))
            operand = "."
        trees.pop()
        tree_count -= 1

    root_id = operand+str(symbol_count)
    if trees[tree_count].root:
        if operand != ".":
            aux = Tree()
            aux.create_node(operand,root_id)
            aux.paste(root_id,symbol_tree)
            symbol_tree = _copy_tree(aux)
            root_id = "."+str(symbol_count)
            operand = "."

    this_tree = Tree()
    this_tree.create_node(operand,root_id)
    this_tree.paste(root_id,trees[tree_count])
    this_tree.paste(root_id,symbol_tree)
    trees[tree_count] = this_tree

def _start_or_chain_syntax_tree(last,symbol,symbol_count,trees,tree_count):
    aux = Tree()
    if trees[tree_count].root:
        root_id = "."+str(symbol_count-1)
        aux.create_node(".",root_id)
        aux.paste(root_id,_copy_tree(trees[tree_count]))
        aux.create_node(last,str(symbol_count-1),parent=root_id)
    else:
        aux.create_node(last,str(symbol_count-1))
    
    tree = Tree()
    root_id = "|"+str(symbol_count)
    tree.create_node("|",root_id)
    tree.paste(root_id,aux)
    tree.create_node(symbol,str(symbol_count),parent=root_id)
    trees[tree_count] = tree

def _copy_tree(tree):
    new = Tree(tree.subtree(tree.root))
    return new

def _condense_expression(expression):
    # Já se considera que a expressão passou pela verificação e está correta

    for k,v in expression.items(): # Expande os grupos
        group_test = False
        new_exp = ""
        exp_stack = [""]
        for symbol in v:
            if group_test: # Expande grupo baseado em Group
                if symbol == "]":
                    group_test = False
                    while exp_stack[-1] != "(":
                        if new_exp[-1] != "(":
                            new_exp += "|"
                        new_exp += exp_stack[-1].value
                        exp_stack.pop()
                    new_exp += ")"
                    exp_stack.pop()
                elif symbol == "z":
                    exp_stack.append(Group.L_ALPHA)
                elif symbol == "Z":
                    exp_stack.append(Group.U_ALPHA)
                elif symbol == "9":
                    exp_stack.append(Group.DIGIT)
            else: # Apenas copia os símbolos se não forem parte de um grupo
                if symbol == "[":
                    group_test = True
                    new_exp += "("
                    exp_stack.append("(")
                else:
                    new_exp += symbol
        expression[k] = new_exp
 
    components = set()
    verified = set()
    while len(verified) < len(expression): # Verifica chamadas de subexpressões
        for k,v in expression.items():
            if k in verified: # Não tem nenhuma subexpressão p/ substituir
                continue
            new_exp = ""
            current_part = ""
            subs_verified = True
            for symbol in v:
                if symbol in Symbols.OPERATIONS.value or symbol in Symbols.GROUP.value:
                    if current_part in expression: # Substitui
                        # Adiciona para o grupo de expressões que não é final
                        components.add(current_part)
                        if current_part not in verified:
                            subs_verified = False
                        current_part = expression[current_part]
                    new_exp += current_part
                    new_exp += symbol
                    current_part = ""
                else:
                    current_part += symbol
            if subs_verified:
                verified.add(k)
            expression[k] = new_exp

    exp = ""
    for k,v in expression.items():
        if k not in components:
            exp += v
            break
    
    if exp == "":
        exp = expression[-1]

    print(exp)
    return "("+exp+")"
