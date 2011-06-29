#!/usr/bin/python

import sys

sys.setrecursionlimit(1200)

func_data = {"I": 1, "zero": 0, "succ": 1, "dbl": 1, "get": 1, "put": 1, "S": 3, "K": 2, "inc": 1, "dec": 1, "attack": 3, "help": 3, "copy": 1, "revive": 1, "zombie": 2}

def too_large(x):
    # damn you Mox Caml & coding monkeys
    return sys.getsizeof(x) > 100000

class Game:
    def simplify(self, v, zomb):
        if type(v) == type(""):
            return self.simplify((v,), zomb)
        if type(v) == type(42):
            return v
        fn = v[0]
        assert(fn in func_data)
        assert(len(v) - 1 <= func_data[fn])
        if len(v) - 1 < func_data[fn]:
            if len(v) == 1:
                return v
            tmp = self.appls
            v1 = (v[0],) + tuple(map(lambda x: self.simplify(x, zomb), v[1:]))
            return v
        if fn == "zero":
            return 0
        self.appls += 1
        if self.appls > 1000:
            raise ValueError
        if fn == "I":
            return self.simplify(v[1], zomb)
        if fn == "succ":
            v1 = self.simplify(v[1], zomb)
            assert(type(v1) == type(42))
            return v1 + 1
        if fn == "dbl":
            v1 = self.simplify(v[1], zomb)
            assert(type(v1) == type(42))
            return v1 * 2
        if fn == "get":
            sn = self.simplify(v[1], zomb)
            assert(self.ar[self.cur_player][sn][0] > 0)
            return self.ar[self.cur_player][sn][1]
        if fn == "put":
            return ("I",)
        if fn == "S":
            f = self.simplify(v[1], zomb)
            g = self.simplify(v[2], zomb)
            x = self.simplify(v[3], zomb)
            f1 = f + (x,)
            if func_data[f1[0]] > len(f1) - 1:
                self.appls += 1
            g1 = g + (x,)
            if func_data[g1[0]] > len(g1) - 1:
                self.appls += 1
            f1 = self.simplify(f1, zomb)
            g1 = self.simplify(g1, zomb)
            if too_large(f1):
                f1 = ("I",)
            if too_large(g1):
                g1 = ("I",)
            fg = f1 + (g1,)
            if func_data[fg[0]] > len(fg) - 1:
                self.appls += 1
            fgres = self.simplify(fg, zomb)
            if too_large(fgres):
                fgres = ("I",)
            return fgres
        if fn == "K":
            return self.simplify(v[1], zomb)
        if fn == "inc":
            sn = self.simplify(v[1], zomb)
            w = self.ar[self.cur_player][sn][0]
            if (w > 0) and (w + 1 - 2 * zomb <= 65535):
                self.ar[self.cur_player][sn][0] += 1 - 2 * zomb
            return ("I",)
        if fn == "dec":
            sn = self.simplify(v[1], zomb)
            w = self.ar[1 - self.cur_player][255 - sn][0]
            if (w > 0) and (w - 1 + 2 * zomb <= 65535):
                self.ar[1 - self.cur_player][255 - sn][0] -= 1 - 2 * zomb
            return ("I",)
        if fn == "attack":
            i = self.simplify(v[1], zomb)
            j = self.simplify(v[2], zomb)
            n = self.simplify(v[3], zomb)
            assert(type(i) == type(42))
            assert(type(j) == type(42))
            assert(type(n) == type(42))
            v = self.ar[self.cur_player][i][0]
            assert(v >= n)
            self.ar[self.cur_player][i][0] -= n
            w = self.ar[1 - self.cur_player][255 - j][0]
            if w > 0:
                w -= n * 9 / 10 * (1 - 2 * zomb)
                if w < 0:
                    w = 0
                if w > 65535:
                    w = 65535
                self.ar[1 - self.cur_player][255 - j][0] = w
            return ("I",)
        if fn == "help":
            i = self.simplify(v[1], zomb)
            j = self.simplify(v[2], zomb)
            n = self.simplify(v[3], zomb)
            assert(type(i) == type(42))
            assert(type(j) == type(42))
            assert(type(n) == type(42))
            v = self.ar[self.cur_player][i][0]
            assert(v > n)
            self.ar[self.cur_player][i][0] -= n
            w = self.ar[self.cur_player][j][0]
            if w > 0:
                w += n * 11 / 10 * (1 - 2 * zomb)
                if w < 0:
                    w = 0
                if w > 65535:
                    w = 65535
                self.ar[self.cur_player][j][0] = w
            return ("I",)
        if fn == "copy":
            sn = self.simplify(v[1], zomb)
            return self.ar[1 - self.cur_player][sn][1]
        if fn == "revive":
            sn = self.simplify(v[1], zomb)
            if self.ar[self.cur_player][sn][0] <= 0:
                self.ar[self.cur_player][sn][0] = 1
            return ("I",)
        if fn == "zombie":
            i = self.simplify(v[1], zomb)
            x = self.simplify(v[2], zomb)
            v = self.ar[1 - self.cur_player][255 - i][0]
            assert(v <= 0)
            self.ar[1 - self.cur_player][255 - i][0] = -1
            self.ar[1 - self.cur_player][255 - i][1] = x
            return ("I",)
        return 42

    def __init__(self, player_cnt = 2):
        self.ar = [[[10000, ("I",)] for i in xrange(256)] for j in xrange(2)]
        self.cur_player = 0
        self.appls = 0
        self.moves_cnt = 0
        self.player_cnt = player_cnt

    def zombies_coming(self):
        for i in xrange(256):
            if self.ar[self.cur_player][i][0] != -1:
                continue
            self.appls = 0
            try:
                #TODO: don't remember, there was something to add here...
                self.simplify(self.ar[self.cur_player][i][1] + (("I",),), 1)
            except:
                pass
            self.ar[self.cur_player][i] = [0, ("I",)]

    def make_turn(self, lr, arg1, arg2):
        self.zombies_coming()
        self.appls = 0
        if 1 <= lr <= 2:
            if lr == 1:
                card, slot = arg1, arg2
            else:
                card, slot = arg2, arg1
            if (0 <= slot <= 255) and (card in func_data):
                old_v, old_slot = self.ar[self.cur_player][slot]
                if lr == 1:
                    new_slot = (card, old_slot)
                    if func_data[new_slot[0]] > len(new_slot) - 1:
                        self.appls += 1
                    else:
                        try:
                            new_slot = self.simplify(new_slot, 0)
                        except:
                            new_slot = ("I",)
                else:
                    try:
                        assert(type(old_slot) == type(()))
                        new_slot = old_slot + (card,)
                        if func_data[new_slot[0]] > len(new_slot) - 1:
                            self.appls += 1
                        else:
                            new_slot = self.simplify(new_slot, 0)
                    except:
                        new_slot = ("I",)
                if too_large(new_slot):
                    new_slot = ("I",)
                self.ar[self.cur_player][slot][1] = new_slot
        if self.player_cnt == 2:
            self.cur_player = 1 - self.cur_player
        if self.cur_player == 0:
            self.moves_cnt += 1
        if self.moves_cnt == 100000:
            self.endgame()

    def endgame(self):
        pass

    def show_state(self):
        for i in xrange(self.player_cnt):
            print >>sys.stderr, i, "player:"
            for j in xrange(256):
                if (self.ar[i][j][1] != ("I",)) or (self.ar[i][j][0] != 10000):
                    print >>sys.stderr, "%d=%s" % (j, self.ar[i][j])
                if type(self.ar[i][j]) == type(()):
                    print >>sys.stderr, "ZOMFG!!!1"

#game = Game(1)
#game.make_turn(2, 0, "help")
#game.make_turn(2, 0, "zero")
#game.make_turn(1, "K", 0)
#game.make_turn(1, "S", 0)
#game.make_turn(2, 0, "succ")
#game.make_turn(2, 0, "zero")
#game.make_turn(2, 1, "zero")
#game.make_turn(1, "succ", 1)
#game.make_turn(1, "dbl", 1)
#game.make_turn(1, "dbl", 1)
#game.make_turn(1, "dbl", 1)
#game.make_turn(1, "dbl", 1)
#game.make_turn(1, "K", 0)
#game.make_turn(1, "S", 0)
#game.make_turn(2, 0, "get")
#game.make_turn(1, "K", 0)
#game.make_turn(1, "S", 0)
#game.make_turn(2, 0, "succ")
#game.make_turn(2, 0, "zero")
#game.show_state()
#
#game = Game(1)
#game.make_turn(2, 0, "S")
#game.make_turn(2, 0, "get")
#game.make_turn(2, 0, "I")
#game.show_state()
#game.make_turn(2, 0, "zero")
#game.show_state()
