#!/usr/bin/python

from botlib import *

log = open("log.txt", "wt")
f = open("mil.txt", "wt")

for s in map(lambda x: x.strip('\n'), open("cmd.txt").xreadlines()):
    ss = s.strip('\n').split()
    if len(s) < 1: continue
    mode = ss[0]
    if mode == "1" or mode == "2":
        print >>f, s
        continue
    buf = apply(eval(mode),ss[1:])
    for lr, arg1, arg2 in buf:
        print >>f, lr, arg1, arg2
f.close()


for s in open("mil.txt").xreadlines():
    try:
        cmd = s.strip('\n').split()
    except:
        continue
    print >>log, "Make command: ", cmd
    log.flush()
    apply(write_turn, cmd)
    read_turn()
