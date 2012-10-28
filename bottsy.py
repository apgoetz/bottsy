#!/usr/bin/env python2

import cgi
import random
import os
from dbclient import *

DBNAME = 'bottsydb'


def update_rank(winner, loser):
    conn = init_db(DBNAME)
    win_score = get_score(conn, int(winner))
    lose_score = get_score(conn, int(loser))
    set_score(conn, int(winner), win_score + 1)
    close_db(conn)

def random_line():
    afile = open('linuxwords')
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line.rstrip()

def display_pair(conn):
    eid = get_open_eid(conn)

    rows = get_active_xc(conn,eid).fetchall()

    id1 = random.choice(rows)[0]
    id2 = random.choice(rows)[0]
    while id1 == id2:
        id2 = random.choice(rows)[0]

    print os.popen("python2 render.py %d" % id1)
    print os.popen("python2 render.py %d" % id2)


    print "<h1>Click on the better thing:</h1>"
    print "<p><a href='bottsy.py?winner={0}&loser={1}'><img src='/bottsy/images/{0}.png'/></a>".format(id1, id2)
    print " or "
    print "<a href='bottsy.py?winner={1}&loser={0}'><img src='/bottsy/images/{1}.png'/></a></p>".format(id1, id2)
    

## BEGINNING OF SCRIPT

conn = init_db(DBNAME)

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers


form = cgi.FieldStorage()
print "<html>"
if "winner" not in form and "loser" not in form:
    print ""
else:
    update_rank(form["winner"].value, form["loser"].value)
    print "<h1> Winner and Loser </h1>"
    print "<p>"
    print form["winner"].value
    print "</p>"

    print "<p><em>"
    print "beat:"
    print "</em></p>"

    print "<p>"
    print form["loser"].value
    print "</p>"

display_pair(conn)

print "</html>"
close_db(conn)


