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
    return False