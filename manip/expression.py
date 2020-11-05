from enum import Enum
from treelib import Node, Tree

class Group(Enum):
    DIGIT = [0,1,2,3,4,5,6,7,8,9]
    L_ALPHA = ['a','b','c','d','e','f','g','h','i','j','k','l','m','n','o',
                'p','q','r','s','t','u','v','x','w','y','z']
    U_ALPHA = ['A','B','C','D','E','F','G','H','I','J','K','L','M','N','O',
                'P','Q','R','S','T','U','V','X','W','Y','Z']
    I_ALPHA = L_ALPHA + U_ALPHA
    L_ALNUM = L_ALPHA + DIGIT
    U_ALNUM = U_ALPHA + DIGIT
    I_ALNUM = I_ALPHA + DIGIT
    
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
    return expression

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
    tree = Tree()
    return tree
