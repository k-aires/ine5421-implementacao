from enum import Enum, auto
from collections import deque

class Error(Enum):
    NONE = auto()
    DEAD = auto()
    ALPHABET = auto()

def verify_input(state_count,alphabet,inp):
    ret = True
    inp = inp.split(",")
    if len(inp) != 3:
        ret = False
    elif not inp[0].isdecimal():
        ret = False
    else:
        inp[0] = int(inp[0])
        if inp[0] >= state_count:
            ret = False
        elif len(inp[1]) != 1:
            ret = False
        elif alphabet.count(inp[1]) == 0 and inp[1] != "":
            ret = False
        else:
            inp[2] = inp[2].split("-")
            for s in inp[2]:
                if s.isdecimal():
                    s = int(s)
                    if s >= state_count:
                        ret = False
                        break
                else:
                    ret = False
                    break
     
    return ret

def format_transitions(transitions):
    trans = {}
    for t in transitions:
        t = t.split(",")
        t[2] = t[2].split("-")
        if len(t[2]) > 1:
            for s in t[2]:
                new_s = t[0]+","+t[1]+","+s
                transitions.append(new_s)
            continue
        t[0] = int(t[0])
        t[2] = int(t[2][0])
        if t[0] not in trans:
            trans[t[0]] = {}
        if t[2] not in trans[t[0]]:
            trans[t[0]][t[2]] = []
        trans[t[0]][t[2]].append(t[1])
    return trans

def recognize_sentence(sentence,automata):
    belongs = Error.DEAD

    current_state = deque([automata["initial"]])
    current_char = deque([0])
    transitions = automata["transitions"]
    while len(current_char) > 0:
        for i in range(current_char[0],len(sentence)):
            char = sentence[i]
            if char not in automata["alphabet"]:
                belongs = Error.ALPHABET
                break
            elif current_state[0] not in transitions:
                break
            else:
                if "&" in automata["alphabet"]: # Aumenta árvore do não-determinismo no epsilon
                    epsilon = _get_keys("&",transitions[current_state[0]])
                    for e in range(0,len(epsilon)):
                        current_state.append(epsilon[e])
                        current_char.append(current_char[0])
                
                next_states = _get_keys(char,transitions[current_state[0]])
                if len(next_states) < 1: # Verifica se tem transições pelo char no estado atual
                    break
                else:
                    current_state[0] = next_states[0]
                    current_char[0] = i+1
                    for j in range(1,len(next_states)): # Aumenta árvore do não-determinístico
                        current_state.append(next_states[j])
                        current_char.append(i+1)
        
        if "&" in automata["alphabet"] and current_state[0] in transitions: # Verifica transições por epsilon no último estado
            epsilon = _get_keys("&",transitions[current_state[0]])
            for e in range(0,len(epsilon)):
                current_state.append(epsilon[e])
                current_char.append(current_char[0])
        
        print(current_state,"\n",current_char)

        if current_char[0] == len(sentence): # Verifica se consome toda a entrada
            if current_state[0] in automata["final"]: # Verifica se termina num estado final
                belongs = Error.NONE
                break

        current_state.popleft() # Para para próximo ramo da árvore
        current_char.popleft()
    
    return belongs

def _get_keys(value,dic):
    key = []
    for k,v in dic.items():
        if value in v:
            key.append(k)
    return key