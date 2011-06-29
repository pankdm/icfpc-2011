from micro_strategy import MicroStrategy
from sys import stderr

#f = open("log.txt", "wt")


class MacroStrategy:
    def __init__(self, first = True):
        self.micro_str = MicroStrategy(first)

    def write_to_log(self, s):
        return
        f.write(str(self.micro_str.game.moves_cnt) + "\t" + s + "\n")
        f.flush()

    def get_turn(self):
        while True:
        #for i in xrange(2):
            try:
                self.write_to_log("Start healing")
                for ar in self.micro_str.heal():
                    for k in xrange(5):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            #if self.micro_str.game.ar[1 - self.micro_str.first][k][1] != ("I",):
                                self.write_to_log("Ressurecting " + str(k))
                                for ar2 in self.micro_str.ressurect(k):
                                    yield ar2
                    yield ar
                self.write_to_log("Healing done")
                self.micro_str.heal_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.heal_slot][1]
                self.write_to_log("Start attack")
                for ar in self.micro_str.attack_best_slot():
                    for k in xrange(5):
                        if self.micro_str.game.ar[1 - self.micro_str.first][k][0] == 0:
                            #if self.micro_str.game.ar[1 - self.micro_str.first][k][1] != ("I",):
                                self.write_to_log("Ressurecting " + str(k))
                                for ar2 in self.micro_str.ressurect(k):
                                    yield ar2
                    yield ar
                self.micro_str.attack_func = self.micro_str.game.ar[1 - self.micro_str.first][self.micro_str.attack_slot][1]
                self.write_to_log("Attack done")
                #self.micro_str.game.whow_state()
            except: #TODO: remove
                yield (1, 'I', 0)
