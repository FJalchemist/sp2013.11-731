#!/bin/sh

./decode_mod.py -s 30 -a 0.3 | ./grade
./decode_mod.py -s 30 -a 0.25 | ./grade
./decode_mod.py -s 30 -a 0.2 | ./grade
./decode_mod.py -s 30 -a 0.15 | ./grade
./decode_mod.py -s 30 -a 0.1 | ./grade
./decode_mod.py -s 30 -a 0.05 | ./grade
