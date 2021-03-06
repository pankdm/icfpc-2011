from ltg_emulator import Game
from sys import stderr
from random import randint

def write_to_log(s):
    return
    f = open("log.txt", "at")
    f.write(s + "\n")
    f.close()

class MicroStrategy:
    def __init__(self, first = True):
        self.game = Game()
        self.N_slot = 1          # CHECK DONE
        self.heal_slot = 4       # CHECK DONE
        self.heal_func = ":)"    # CHECK DONE
        self.attack_func = ":)"  # CHECK DONE
        self.zombie_func = ":)"  # CHECK DONE
        self.a_z_func = ":)"     # CHECK DONE
        self.first = int(first)  #
        self.target_slot = 2     #
        self.attack_slot = 3     #
        self.itr = 6             #
        self.zombie_slot = 5     #

    def make_zombie_cell(self):
        zombie = []
        zombie += parse_block("""
        2 zombie
        1 S
        2 put
        """)
        zombie += compose([(1, "get")] + gen_fn(self.target_slot))
        res = add_slot(self.zombie_slot, zombie)
        return res

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
            if (self.game.moves_cnt < 60) and (bt == 255):
                bt = 2
            #print >>stderr, self.game.ar[self.first][:5]
            return bt
        return 255

    def ressurect(self, k):
        #print >>stderr, "DEBUG: reviving", k
        #print >>stderr, self.itr
        while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
            self.itr += 1
            #print >>stderr, self.itr

        revive = gen_num(k)
        revive += parse_block("""
        1 revive
        """)
        res = add_slot(self.itr, revive)
        return res

    def attack_best_slot(self):
        NNN = 2**13
        res = []

        attack_slot = self.attack_slot
        N_slot = self.N_slot
        target_slot = self.target_slot

        if self.game.ar[1 - self.first][N_slot][0] <= 0:
            #print >>stderr, "DEBUG: reviving N_slot"
            #print >>stderr, self.itr
            while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
                self.itr += 1
                #print >>stderr, self.itr
            revive = parse_block("""
            2 zero
            1 succ
            1 revive
            """)
            res += add_slot(self.itr, revive)

        if self.game.ar[1 - self.first][target_slot][0] <= 0:
            #print >>stderr, "DEBUG: reviving target_slot"
            while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
                self.itr += 1
            revive = parse_block("""
            2 zero
            1 succ
            1 succ
            1 revive
            """)
            res += add_slot(self.itr, revive)

        best_target = 255 - self.select_best_slot()
        #res += [(1, "zero", target_slot)]
        res += add_slot(target_slot, gen_num2(self.game.ar[1-self.first][target_slot][1],best_target))
        tmp = self.game.ar[1 - self.first][N_slot][1]
        if (type(tmp) != type(42)) or (tmp < 11000) or (tmp > 17000):
            #print >>stderr, "DEBUG: create N_slot"
            #res += [(1, "zero", N_slot)]
            gn = gen_num2(tmp, NNN)
            #print >>stderr, gn
            res += add_slot(N_slot, gn)
            #res += add_slot(N_slot, gen_num(best_target))
            #res += add_slot(target_slot, get_from(N_slot))
            #res += add_slot(N_slot, parse_block("1 dbl\n" * 6))

        if self.game.ar[1 - self.first][attack_slot][0] <= 0:
            #print >>stderr, "DEBUG: moving attack_slot"
            while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
                self.itr += 1
            attack_slot = self.itr
            self.attack_slot = self.itr
            if self.itr < 255:
                self.itr += 1

        if self.game.ar[1 - self.first][attack_slot][1] not in [self.a_z_func, self.attack_func]:
            #print >>stderr, "DEBUG: create attack_slot"
            attack = []
            attack += parse_block("""
            2 attack
            2 zero
            """)

            # assert target_slot = N_slot + 1
            attack += compose( [(1, "get")] + gen_fn(1) )
            attack += parse_block("""
            1 S
            2 get
            """)

            attack += compose( gen_fn(N_slot) )
            res += add_slot(attack_slot, attack)
        if (self.using_zombie):
            if self.game.ar[1 - self.first][attack_slot][1] != self.a_z_func:
                za = []
                za += parse_block("1 S\n")
                za += compose([(1,"get")] + gen_fn(self.zombie_slot))
                za += parse_block("""
                1 S
                2 I
                """)
                res += add_slot(attack_slot, za)

        res += add_slot(0, get_from(attack_slot))
        res.append((2, 0, "zero"))

        if target_slot < 255:
            res += add_slot(target_slot, [(1, "succ")])

            res += add_slot(0, get_from(attack_slot))
            res.append((2, 0, "zero"))

        return res

    def heal(self):
        NNN = 2**13
        res = []
        N_slot = self.N_slot
        heal_slot = self.heal_slot
        target_slot = self.target_slot

        if self.game.ar[1 - self.first][N_slot][0] <= 0:
            #print >>stderr, "DEBUG heal: reviving N_slot"
            while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
                self.itr += 1
            revive = parse_block("""
            2 zero
            1 succ
            1 revive
            """)
            res += add_slot(self.itr, revive)

        tmp = self.game.ar[1 - self.first][N_slot][1]
        if (type(tmp) != type(42)) or (tmp < 8000) or (tmp > 17000):
            #print >>stderr, "DEBUG heal: create N_slot"
            res += [(1, "zero", N_slot)]
            #res += add_slot(N_slot, gen_num(NNN))
            tmp2 = self.game.ar[1-self.first][target_slot][1]
            if self.game.moves_cnt <40:
                res += add_slot(N_slot, gen_num(252))
                res += add_slot(target_slot, get_from(N_slot))
                res += add_slot(N_slot, parse_block("1 dbl\n" * 5))
            else :
                res += add_slot(N_slot, gen_num2(tmp,10000))

        if self.game.ar[1 - self.first][heal_slot][0] <= 0:
            #print >>stderr, "DEBUG heal: move heal_slot"
            while (self.game.ar[1 - self.first][self.itr][0] <= 0) and (self.itr < 254):
                self.itr += 1
            heal_slot = self.itr
            self.heal_slot = self.itr
            if self.itr < 255:
                self.itr += 1

        if self.game.ar[1 - self.first][heal_slot][1] != self.heal_func:
            #print >>stderr, "DEBUG heal: create heal_slot"
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

        res += add_slot(0, get_from(heal_slot) )
        res.append((2, 0, "zero"))
        if self.game.ar[1 - self.first][N_slot][1] < 15000:
            res += add_slot(N_slot, parse_block("1 dbl"))
        return res

def gen_num2(a, b):
    print >>stderr, "GET_NUM", a, b
    if a == ('I',):
        text = gen_num2(0, b)
        #print text
        return  [(2, 'zero')] + text
    if type(a) != type(42):
        text = gen_num2(0, b)
        return  [(1, 'zero'), (2, 'zero')] + text
    if a>b:
        text = gen_num2(0, b)
        return  [(1, 'zero'), (2, 'zero')] + text
    if a==b:
        return []
    if b > 1000:
        text=[]
        if  a==0:
            a+=1
            text = [(1, 'succ')]
        while a<b:
            a*=2
            text = text + [(1, 'dbl')]
        return text

    minstep = 0
    curh = {a : [] }
    maxsteps=4+len(gen_num(b))
    for i in range(1,maxsteps+1):
      nexth={}
      for k in curh.keys():
          if k + 1 <= b :
              nexth[k + 1] = curh[k] + [(1, "succ") ]
          if 2 * k <= b :
              nexth[2 * k] = curh[k] + [(1,"dbl")]
      if nexth.has_key(b) :
          return nexth[b]
      curh=nexth
    return [(1,'zero'), (2, 'zero')] + gen_num2(0,b)



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

