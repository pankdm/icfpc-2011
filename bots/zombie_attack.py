#!/usr/bin/python

from botlib import *
from sys import argv

#debug = True
debug = False

if argv[1] == "1":
    read_turn()


res = []

N_slot = 1
target_slot = 2
attack_slot = 3
heal_slot = 4
zombie_slot = 5


res += add_slot(N_slot, gen_num(252))

res += add_slot(target_slot,  get_from(N_slot) )
res += add_slot(N_slot, parse_block("1 dbl\n" * 5))

# now we have numbers 8K,252 

if debug: print >>stderr, "we have 8K && 252 at ", len(res)

heal = []

heal += parse_block("""
2 help
2 zero
2 zero
""")

heal += compose( [(1, "get")] +  gen_fn(N_slot) )
heal += parse_block("""
1 S
2 get
1 S
2 I
""")
res += add_slot(heal_slot, heal)

if debug: print >>stderr, 'created heal at', len(res)


#launch heal
res += add_slot(0,  get_from(heal_slot) )
res.append ((2, "0", "zero") )

if debug: print >>stderr, "healed at", len(res)

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

if debug: print >>stderr, "created attack at", len(res)

res.append ((1, "dbl", N_slot) )

ind = 0
kill_list = [3,4,4,8,8,16,32,64,128,255] + ([255, ] * 1000 )
killstart = kill_list[ind]
for target in xrange(256-killstart,256,2):

    res += add_slot(0, get_from(attack_slot))
    res.append((2, "0", "zero"))


    if debug: print >>stderr, 'attacked ', target, 'at ', len(res)
    
    res += add_slot(target_slot, [(1, "succ")])

    res += add_slot(0, get_from(attack_slot))
    res.append((2, "0", "zero"))

    if debug: print >>stderr, 'attacked ', target + 1, 'at ', len(res)

    res += add_slot(0,  get_from(heal_slot) )
    res.append ((2, "0", "zero") )

    if debug: print >>stderr, 'healed after at ', len(res)

    if (target < 255): res += add_slot(target_slot, [(1, "succ")])
ind += 1
killstart = kill_list[ind]

res.append((1, "zero", target_slot)) ## raise error
res += add_slot(target_slot, gen_num(255 - killstart))


if debug: print >> stderr, "have number", 255 - killstart, ' at ', len(res)

## create zombie 
zombie = [] 
zombie += parse_block("""
2 zombie
1 S
2 get 
""")

zombie += compose( [(1, "get")] +  gen_fn(target_slot) )

res += add_slot(zombie_slot,zombie)


if debug: print >> stderr, "created zombie at", len(res)
### create zombie and attack in attack_slot

za =[]
za +=parse_block("1 S\n")
za +=compose( [(1,"get")] +gen_fn(zombie_slot))

za += parse_block("""
1 S
2 I
""")

res +=add_slot(attack_slot,za)

while (len(res) < 100100):
    for target in xrange(256-killstart,256,2):

        res += add_slot(0, get_from(attack_slot))
        res.append((2, "0", "zero"))

        #res += add_slot(0, get_from(zombie_slot))
        #res.append((2, "0", "zero"))
        
        if debug: print >>stderr, 'attacked and zombified', target, ' at ', len(res)

        res += add_slot(target_slot, [(1, "succ")])

        res += add_slot(0, get_from(attack_slot))
        res.append((2, "0", "zero"))

        if debug: print >>stderr, 'attacked and zombified', target + 1, ' at ', len(res)

        #res += add_slot(0, get_from(zombie_slot))
        #res.append((2, "0", "zero"))
        #print >>stderr, 'attacked ', target, 'at ', len(res)

        res += add_slot(0,  get_from(heal_slot) )
        res.append ((2, "0", "zero") )

        if debug: print >>stderr, 'healed after at', len(res)

        if (target < 255): res += add_slot(target_slot, [(1, "succ")])
    res.append((1, "zero", target_slot)) ## raise error
    if debug: print >>stderr, "raise error at ", len(res)
    ind += 1
    killstart = kill_list[ind]
    res += add_slot(target_slot, gen_num(255 - killstart))
    
    if debug: print >>stderr, "generated new target at ", len(res)

    if killstart > 4: debug = False

#for cmd in res:
#    print >>stderr, "cmd: ", cmd

execute(res)
