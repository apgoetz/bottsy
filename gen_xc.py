#!/usr/bin/python2

from dbclient import *;
import random;

if(len(sys.argv) < 2):
    print "Must supply eid"
    sys.exit(-1)

DB = 'bottsydb'
EID = int(sys.argv[1])

NUM_XC = 16



#chromosome description
# order: line_max, line_min, arc_ang_max, arc_ang_min, arc_dist_max, arc_dist_min, turn_max, turn_min
# '[[25, 5, 360, -360, 25, 5, 70, -70], [[[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]], [[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]]]]'

def build_xc(c, eid):
    line_max = random.randint(1, 50)
    line_min = random.randint(0, line_max)
    
    arc_ang_max = random.randint(-360, 360)
    arc_ang_min = random.randint(-360, arc_ang_max)

    arc_dist_max = random.randint(1, 50)
    arc_dist_min = random.randint(0, arc_dist_max)

    turn_max = random.randint(-360, 360)
    turn_min = random.randint(-360, turn_max)

    xc_str = '[[%d, %d, %d, %d, %d, %d, %d, %d], [[[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]], [[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]]]]' % (line_max, line_min, arc_ang_max, arc_ang_min, arc_dist_max, arc_dist_min, turn_max, turn_min)

    add_xc(c, eid, 1, xc_str, 1, 1, 1)

    

    



conn = init_db(DB)
for i in range(NUM_XC):
    build_xc(conn, EID)
close_db(conn)

