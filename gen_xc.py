#!/usr/bin/python2
import json
from dbclient import *;
import random;
import pickle
import os

DB = 'bottsydb'






#chromosome description
# order: line_max, line_min, arc_ang_max, arc_ang_min, arc_dist_max, arc_dist_min, turn_max, turn_min
# '{[25, 5, 360, -360, 25, 5, 70, -70}, [[[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]], [[0.33, 0.33, 0.33], [0.33, 0.33, 0.33], [0.33, 0.33, 0.33]]]]'

def build_xc(c, eid):
    line_max = random.randint(1, 50)
    line_min = random.randint(0, line_max)
    
    turn_max = random.randint(-360, 360)
    turn_min = random.randint(-360, turn_max)

    rt_max = random.randint(7000,10000)
    rt_min = random.randint(4000,rt_max)

    sense = random.randint(100,250)   

    L = 0.5
    T = 0.5

    xc_str = {'light':{'dMax':line_max,'dMin':line_min, 'phiMax':turn_max,'phiMin':turn_min, 'rtMax':rt_max, 'rtMin':rt_min, 'lSense':sense,'weights':{'line':{'L':L,'T':T},'turn':{'L':L,'T':T}}},'dark':{'dMax':line_max,'dMin':line_min, 'phiMax':turn_max,'phiMin':turn_min, 'rtMax':rt_max, 'rtMin':rt_min, 'lSense':sense,'weights':{'line':{'L':L,'T':T},'turn':{'L':L,'T':T}}}}
    add_xc(c, eid, 1, pickle.dumps(xc_str), 1, 1, 100)
    

    



conn = init_db(DB)

if(len(sys.argv) < 2):
    num_elements = 100
else:
    num_elements = int(sys.argv[1])

add_exp(conn, "test", "")
EID = get_open_eid(conn)
print "New EID: " + str(EID)

for i in range(num_elements):
    build_xc(conn, EID)
    
    
close_db(conn)

