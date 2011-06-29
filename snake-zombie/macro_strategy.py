from micro_strategy import MicroStrategy
from sys import stderr

class MacroStrategy:
    def __init__(self, first = True):
        self.micro_str = MicroStrategy(first)

    def get_turn(self):
        while True:
        #for i in xrange(2):
            try:
                for ar in self.micro_str.heal():
                    for k in xrange(5):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            if self.micro_str.game.ar[1 - self.micro_str.first][k][1] != ("I",):
                                for ar2 in self.micro_str.ressurect(k):
                                    yield ar2
                    yield ar
                self.micro_str.heal_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.heal_slot][1]
                for ar in self.micro_str.attack_best_slot():
                    for k in xrange(5):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            if self.micro_str.game.ar[1 - self.micro_str.first][k][1] != ("I",):
                                for ar2 in self.micro_str.ressurect(k):
                                    yield ar2
                    yield ar
                self.micro_str.attack_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.attack_slot][1]
                #self.micro_str.game.show_state()
            except EOFError: #TODO: remove
                yield (1, 'I', 0)
