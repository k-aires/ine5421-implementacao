from enum import Enum, auto

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
        trans[t[0]][t[2]] = t[1]
    return trans

def recognize_sentence(sentence,automata):
    belongs = Error.NONE
    current_state = automata["initial"]
    transitions = automata["transitions"]
    for char in sentence:
        if char not in automata["alphabet"]:
            belongs = Error.ALPHABET
            break
        elif current_state not in transitions:
            belongs = Error.DEAD
            break
        elif char not in transitions[current_state].values():
            belongs = Error.DEAD
            break
        else:
            current_state = _get_key(char,transitions[current_state])
    
    return belongs

def _get_key(value,dic):
    key = -1
    for k,v in dic.items():
        if v == value:
            key = k
            break
    return key