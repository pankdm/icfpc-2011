#!/usr/bin/python

from botlib import *


res = []

N_slot = 1
target_slot = 2
attack_slot = 3
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

#print >>stderr, 'created heal at', len(res)


res += add_slot(target_slot, gen_num(255))


res += add_slot(0,  get_from(heal_slot) )
res.append ((2, "0", "zero") )

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

#print >>stderr, 'healed at', len(res)



res.append ((1, "dbl", N_slot) )

#print >>stderr, 'killed 0 at', len(res)


while (len(res) < 100100):
    res += add_slot(target_slot, gen_num(0)) # raise error
    res += add_slot(target_slot, gen_num(0)) 
    for target in xrange(256):

        res += add_slot(0, get_from(attack_slot))
        res.append((2, "0", "zero"))

        #print >>stderr, 'attacked ', target, 'at ', len(res)

        res += add_slot(0,  get_from(heal_slot) )
        res.append ((2, "0", "zero") )

        #print >>stderr, 'healed after at', len(res)

        if (target < 255): res += add_slot(target_slot, [(1, "succ")])

#for cmd in res:
#    print >>stderr, "cmd: ", cmd

execute(res)
