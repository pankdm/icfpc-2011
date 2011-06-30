#!/usr/bin/python

from botlib import *


res = []

attack_slot = 0
N_slot = 1
target_slot = 2
heal_slot = 4

shot = 2**13
res += add_slot(N_slot, gen_num(2**13))

heal = []
heal += parse_block("""
2 help
2 zero
2 zero
""")
#heal += compose(gen_fn(8192))
#heal += compose( [(1, "get"), (1, "succ")] ) # depends on N_slot
heal += compose( [(1, "get")] +  gen_fn(N_slot) )


heal += parse_block("""
1 S
2 get
1 S
2 I
""")
#res += gen_num(1, 125) 

#res += parse_block("""
#2 zero
#1 I
#1 I
#""")

res += add_slot(heal_slot, heal)
res += add_slot(target_slot, gen_num(255))

res += add_slot(0,  get_from(heal_slot) )
res.append ((2, "0", "zero") )

res += add_slot(N_slot, parse_block("1 dbl"))

attack = []
attack += parse_block("""
2 attack
2 zero
""")

attack += compose( [(1, "get")] + gen_fn(target_slot) )
attack += parse_block("2 zero")

attack += compose( [(1, "get")] + gen_fn(N_slot) )
attack += parse_block("2 zero")

res +=  add_slot(attack_slot, attack)

while (len(res) < 100100):
    res += add_slot(target_slot, gen_num(0)) # raise error
    res += add_slot(target_slot, gen_num(0)) 
    for target in xrange(256):
        attack = []
        attack += parse_block("""
        2 attack
        2 zero
        """)

        attack += compose( [(1, "get")] + gen_fn(target_slot) )
        attack += parse_block("2 zero")

        attack += compose( [(1, "get")] + gen_fn(N_slot) )
        attack += parse_block("2 zero")

        res +=  add_slot(attack_slot, attack)

        if (target < 255): res += add_slot(target_slot, [(1, "succ")])
        
        res += add_slot(0,  get_from(heal_slot) )
        res.append ((2, "0", "zero") )


for cmd in res:
    print >>stderr, "cmd: ", cmd

execute(res)
