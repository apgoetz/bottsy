#!/usr/bin/env python2

import cgi
import random
import os
import math
from dbclient import *

DBNAME = 'bottsydb'

def calc_elo(a, b):
    value = 1.0/(1 + math.pow(10,(b-a)/400))
    return value

def calc_c(rating):
    if rating < 2000:
        return 30
    elif rating < 2400:
        return 130 - rating/20.0
    else:
        return 10
    

def update_rank(winner, loser):
    conn = init_db(DBNAME)
    win_id = int(winner)
    lose_id = int(loser)
    win_score = get_score(conn, win_id)
    lose_score = get_score(conn, lose_id)
    
    win_exp = calc_elo(win_score, lose_score)
    lose_exp = calc_elo(lose_score, win_score)

    win_new_score = win_score + calc_c(win_id) * (1 - calc_elo(win_id, lose_id))
    los_new_score = lose_score + calc_c(lose_id) * (0 - calc_elo(lose_id,win_id))

    if win_new_score < 0:
        win_new_score = 0

    if los_new_score < 0:
        los_new_score = 0

    set_score(conn, win_id, win_new_score)
    set_score(conn, lose_id, los_new_score)

    
    close_db(conn)


def display_pair(conn):
    eid = get_open_eid(conn)

    rows = get_active_xc(conn,eid).fetchall()

    id1 = random.choice(rows)[0]
    id2 = random.choice(rows)[0]
    while id1 == id2:
        id2 = random.choice(rows)[0]

    os.system("python2 render.py %d" % id1)
    os.system("python2 render.py %d" % id2)



    print "<p style='float: left'><b>{0}</b><br/><a href='bottsy.py?winner={0}&loser={1}'><img src='/bottsy/images/{0}.png'/></a></p>".format(id1, id2)

    print "<p style='float: right'><b>{1}</b><br/><a href='bottsy.py?winner={1}&loser={0}'><img src='/bottsy/images/{1}.png'/></a></p>".format(id1, id2)
    

## BEGINNING OF SCRIPT

conn = init_db(DBNAME)

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers


form = cgi.FieldStorage()

print "<html>"
print "<h2>Bottsy: Robot art Fight!</h2>"
if "winner" not in form and "loser" not in form:
    print "<h2>Click on the better thing:</h2>"
else:
    win_id = int(form["winner"].value)
    lose_id = int (form["loser"].value)
    update_rank(win_id, lose_id)
    print "<div><h2> Winner and Loser </h2>"
    print "<p>"
    print "<a href=/bottsy/show.py?id={0}>{0}</a>, new score {1}".format(win_id, get_score(conn, win_id))


    print "<em>"
    print "beat:"
    print "</em>"


    print "<a href=/bottsy/show.py?id={0}>{0}</a>, new score {1}".format(lose_id, get_score(conn, lose_id))
    print "</p></div>"


display_pair(conn)

print "<div style='clear:both'><a href='/bottsy/rank.py'>Ranking</a></div>"

print "</html>"
close_db(conn)


