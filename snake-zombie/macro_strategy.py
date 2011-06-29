from micro_strategy import MicroStrategy
from sys import stderr

class MacroStrategy:
    def __init__(self, first = True):
        self.micro_str = MicroStrategy(first)

    def get_turn(self):
        while True:
        #for i in xrange(2):
            for ar in self.micro_str.heal():
                yield ar
            for ar in self.micro_str.attack_best_slot():
                yield ar
