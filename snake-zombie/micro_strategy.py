from ltg_emulator import Game
from sys import stderr

def write_to_log(s):
    return
    f = open("log.txt", "at")
    f.write(s + "\n")
    f.close()

class MicroStrategy:
    def __init__(self, first = True):
        self.game = Game()
        self.N_slot = 1
        self.heal_slot = 4
        self.heal_func = ":)"
        self.first = int(first)
        self.target_slot = 2
        self.attack_slot = 0
        self.tmp = 0

    def select_best_slot(self):
        def without_heal(func):
            return str(func).find("help") == -1

        ind = [[], [], [], []]
        ind[0] = filter(lambda x: self.game.ar[self.first][x][0] > 0, range(256))
        ind[1] = filter(lambda x: self.game.ar[self.first][x][1] != ("I",), ind[0])
        ind[2] = filter(lambda x: self.game.ar[self.first][x][0] <= 16000, ind[1])
        ind[3] = filter(lambda x: without_heal(self.game.ar[self.first][x][1]), ind[2])
        for i in xrange(3, -1, -1):
            if len(ind[i]) == 0:
                continue
            bt = ind[i][-1]
            write_to_log("BEST TARGET: %d" % bt)
            if (self.game.moves_cnt == 0) and (bt == 255):
                bt = 2
            return bt

    def attack_best_slot(self):
        res = []
        attack = []
        attack += parse_block("""
        2 attack
        2 zero
        """)

        attack_slot = self.attack_slot
        N_slot = self.N_slot # TODO: if it is dead
        target_slot = self.target_slot  # TODO: if it is dead
        best_target = 255 - self.select_best_slot()
        res.append((1, "zero", target_slot))
        res += add_slot(target_slot, gen_num(best_target))
        attack += compose([(1, "get")] + gen_fn(target_slot))
        attack += parse_block("2 zero")

        attack += compose([(1, "get")] + gen_fn(N_slot))
        attack += parse_block("2 zero")

        res += add_slot(attack_slot, attack)

        #res.append((2, 0, "zero"))
        return res

    def heal(self):
        NNN = 2**13
        res = []
        N_slot = self.N_slot
        heal_slot = self.heal_slot

        if self.game.ar[1 - self.first][N_slot][1] not in [NNN, 2 * NNN]:
            res += add_slot(N_slot, gen_num(NNN))

        if self.game.ar[1 - self.first][heal_slot][1] != self.heal_func:
            heal = []
            heal += parse_block("""
            2 help
            2 zero
            2 zero
            """)
            heal += compose([(1, "get")] + gen_fn(N_slot))
            heal += parse_block("""
            1 S
            2 get
            1 S
            2 I
            """)
            res += add_slot(heal_slot, heal)
            self.heal_func = ('S', ('S', ('S', ('K', ('S', ('K', ('help', 'zero', 'zero')), 'get')), 'succ'), 'get'), 'I')
        res += add_slot(0, get_from(heal_slot) )
        res.append((2, 0, "zero"))
        if self.game.ar[1 - self.first][N_slot][1] != 2 * NNN:
            res += add_slot(N_slot, parse_block("1 dbl"))
        return res

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
        assert(str(cmd[0]) == "1")
        res.append((1, "K"))
        res.append((1, "S"))
        res.append((2, cmd[1]))
    return res

def add_slot(slot, commands):
    res = []
    for cmd in commands:
        res.append(reorder_cmd(slot, *cmd))
    return res

def reorder_cmd(slot, mode, name):
    if str(mode) == "1":
        return (int(mode), name, int(slot))
    else:
        return (int(mode), int(slot), name)

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

