# Importa módulo para interface no terminal
from simple_term_menu import TerminalMenu

# Importa arquivos de lógica
import automata
import expression
import grammar

def initial_menu():
    print("Você está no menu inicial. Para procurar a opção desejada, ",
            "digite /.\nPor favor, selecione a opção desejada.")
    t_menu = TerminalMenu(["Novo input","Abrir arquivo","Sair"])
    return t_menu.show()

def input_menu():
    t_menu = TerminalMenu(["Autômato finito","Gramática regular",
        "Expressão regular","Gramática livre de contexto","Menu","Sair"])
    return t_menu.show()

def open_file_menu():
    _nope()

def save_file_menu():
    _nope()

def finite_automata_menu():
    t_menu = TerminalMenu(["Conversão para AFD","Conversão para GR",
        "Reconhecimento de sentença","Minimização","União","Interseção",
        "Editar","Exportar","Menu","Sair"])
    return t_menu.show()

def regular_grammar_menu():
    t_menu = TerminalMenu(["Conversão para AFND",
        "Editar","Exportar","Menu","Sair"])
    return t_menu.show()

def regular_expression_menu():
    t_menu = TerminalMenu(["Conversão para AFD",
        "Editar","Exportar","Menu","Sair"])
    return t_menu.show()

def context_free_grammar_menu():
    t_menu = TerminalMenu(["Forma normal de Chomsky",
        "Eliminação de recursão à esquerda","Fatoração",
        "Editar","Exportar","Menu","Sair"])
    return t_menu.show()

def automata_input():
    print("Input para autômato finito.")
    aut = {}
    while True: # Pega primeiro input, de número de estados
        state_count = input("Número de estados: ")
        if state_count.isdecimal():
            aut["count"] = int(state_count)
            break
        else:
            _invalid()
    
    while True: # Pega segundo input, do estado inicial
        initial_state = input("Estado inicial: ")
        if not initial_state.isdecimal():
            _invalid()
        else:
            initial_state = int(initial_state)
            if initial_state >= aut["count"]:
                _invalid()
            else:
                aut["initial"] = initial_state
                break

    while True: # Pega terceiro input, dos estados finais
        final_states = input("Estados finais: ").split(",")
        nerr = True
        for s in final_states:
            if not s.isdecimal():
                _invalid()
                nerr = False
                break
            s = int(s)
            if s >= aut["count"]:
                _invalid()
                nerr = False
                break
        if nerr:
            aut["final"] = final_states
            break

    while True: # Pega quarto input, do alfabeto
        alphabet = input("Alfabeto: ").split(",")
        nerr = True
        for a in alphabet:
            if len(a) != 1:
                _invalid()
                nerr = False
                break
        if nerr:
            aut["alphabet"] = alphabet
            break

    print("Transições (para sair do input, digite .):")
    transitions = []
    while True:
        inp = input()
        if inp == ".":
            break
        if automata.verify_input(aut["count"],aut["alphabet"],inp):
            transitions.append(inp)
        else:
            _invalid()
    aut["transitions"] = automata.format_transitions(transitions)

    return aut

def grammar_input(grammar_type):
    # grammar_type: 0 indica regular, 1 indica livre de contexto
    print("Input para gramáticas. Para sair do input, digite .")
    gram = []
    while True:
        inp = input()
        if inp == ".":
            break
        
        if grammar.verify_input(grammar_type,inp):
            gram.append(inp)
        else:
            _invalid()
        gram.append(inp)
    return gram

def expression_input():
    print("Input para expressões. Para sair do input, digite .")
    exp = []
    while True:
        inp = input()
        # Verifica saída do input
        if inp == ".":
            break

        # Verifica se expressão é válida
        if expression.verify_input(inp):
            exp.append(inp)
        else:
            _invalid()
    exp = expression.format_expression(exp)
    return exp

def _invalid():
    print("Input inválido. Por favor, tente novamente.")

def _nope():
    print("Não implementado.")
