from sys import  stdout, stderr

def get_line():
    try:
        return raw_input().strip('\n')
    except EOFError:
        exit()

def read_turn():
    lt = get_line()
    arg1 = get_line()
    arg2 = get_line()
    return (lt, arg1, arg2)

def write_turn(lt, arg1, arg2):
    stdout.write(str(lt) + "\n")
    stdout.write(str(arg1) + "\n")
    stdout.write(str(arg2) + "\n")
    stdout.flush()

def gen_num(n):
    n = int(n)
    res = []
    while True:
        if n % 2 == 1: res.append( (1, "succ") )
        if n == 0 or n == 1: break
        res.append( (1, "dbl") )
        n /= 2
    res.append( (2, "zero") )
    res.reverse()
    return res


def gen_fn(n):
    n = int(n)
    res = []
    while True:
        if n % 2 == 1: res.append( (1, "succ") )
        if n == 0 or n == 1: break
        res.append( (1, "dbl") )
        n /= 2
    return res

def compose(commands):
    res = []
    for cmd in commands:
        assert( str(cmd[0]) == "1" )
        res.append( (1, "K") )
        res.append( (1, "S") )
        res.append( (2, cmd[1]) )
    return res

def add_slot(slot, commands):
    res = []
    for cmd in commands:
        res.append(reorder_cmd(slot, *cmd))
    return res

def reorder_cmd(slot, mode, name):
    if str(mode) == "1":
        return (mode, name, slot)
    else:
        return (mode, slot, name)

def parse_block(block):
    res = []
    for s in block.split("\n"):
        args = s.split()
        if len(args) != 2:continue
        res.append(tuple(args))
    return res

def add_block2(slot, block):
    return add_slot(slot, parse_block(block))

def add_block(block):
    res = []
    for s in block.split("\n"):
        args = s.split()
        if len(args) != 3:
            continue
        res.append(tuple(args))
    return res

def get_from(slot):
    res = []
    res += gen_num(slot)
    res.append( (1, "get" ) )
    return res

def execute(commands):
    for cmd in commands:
        apply(write_turn, cmd)
        read_turn()
