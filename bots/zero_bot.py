#!/usr/bin/python

from sys import argv, stderr
from botlib import read_turn, write_turn

if argv[1] == "1": read_turn()

while (True):
    write_turn("1", "I", "0")
    read_turn()
