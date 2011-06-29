from micro_strategy import MicroStrategy
from sys import stderr

class MacroStrategy:
    def __init__(self, first = True):
        self.micro_str = MicroStrategy(first)
        self.micro_str.using_zombie = False

    def checkForRevive(self):
        if self.micro_str.using_zombie:
            return
        for i in xrange(256):
            if 0 < self.micro_str.game.ar[self.micro_str.first][i][0] <= 10:
                self.micro_str.using_zombie = True
                return

    def get_turn(self):
        while True:
            try:
                for ar in self.micro_str.heal():
                    for k in xrange(6):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            for ar2 in self.micro_str.ressurect(k):
                                yield ar2
                    yield ar
                self.micro_str.heal_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.heal_slot][1]
                if self.micro_str.using_zombie:
                    if self.micro_str.zombie_func != self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.zombie_slot][1]:
                        for ar in self.micro_str.make_zombie_cell():
                            for k in xrange(6):
                                if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                                    for ar2 in self.micro_str.ressurect(k):
                                        yield ar2
                            yield ar
                        self.micro_str.zombie_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.zombie_slot][1]
                for ar in self.micro_str.attack_best_slot():
                    for k in xrange(6):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            for ar2 in self.micro_str.ressurect(k):
                                yield ar2
                    if ar == "SAVEATTACK":
                        self.micro_str.attack_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.attack_slot][1]
                    elif ar == "SAVEAZ":
                        self.micro_str.a_z_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.attack_slot][1]
                    else:
                        yield ar
            except:# EOFError:
                yield (1, 'I', 0)
