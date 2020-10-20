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
        t[2] = t.split("-")
        if len(t[2]) > 1:
            for s in t[2]:
                new_s = t[0]+","+t[1]+","+s
                print(new_s)
                transitions.append(new_s)
            continue
        t[0] = int(t[0])
        t[2] = int(t[2])
        if t[0] not in trans:
            trans[t[0]] = {}
        trans[t[0]][t[2]] = t[1]
    return trans