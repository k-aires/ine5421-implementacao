# Importa arquivos
import io_terminal
import expression
import grammar
import automata

def menu():
    # Chama interface do menu
    inp = io_terminal.initial_menu()

    # Lógica da opção escolhida
    if inp == 0:
        input_menu()
    elif inp == 1:
        file_menu(True)

def input_menu():
    inp = io_terminal.input_menu()
    if inp == 0:
        finite_automata()
    elif inp == 1:
        regular_grammar()
    elif inp == 2:
        regular_expression()
    elif inp == 3:
        context_free_grammar()
    elif inp == 4:
        menu()

def file_menu(opening):
    if opening:
        io_terminal.open_file_menu()
    else:
        io_terminal.save_file_menu()

def finite_automata():
    aut = io_terminal.automata_input()

def regular_grammar():
    gram = io_terminal.grammar_input()

def regular_expression():
    exp = io_terminal.expression_input()

def context_free_grammar():
    io_terminal._nope()
    menu()

if __name__ == "__main__":
    menu()
