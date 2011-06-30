#!/usr/bin/python

from botlib import *

res = []

N_slot = 1
res += add_slot(N_slot, gen_num(2**13))

heal = []
heal += parse_block("""
2 help
2 zero
2 zero
""")
#heal += compose(gen_fn(8192))
heal += compose( [(1, "get"), (1, "succ")] ) # depends on N_slot

# recursion
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

heal_slot = 2
res += add_slot(heal_slot, heal)

for i in xrange(1):
    res += add_slot(0,  get_from(heal_slot) )
    res.append ((2, "0", "zero") )


for cmd in res:
    print >>stderr, "cmd: ", cmd

execute(res)
