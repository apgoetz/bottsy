#!/usr/bin/python2
import cgi
from dbclient import *

conn = init_db('bottsydb')

eid = get_open_eid(conn)

rows = get_ranked_xc(conn, eid).fetchall()

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print '<html>'

print '<h1>Current Robot Ranking:</h1>'

for r in rows:
    score = get_score(conn, r[0])
    print "<a href='/bottsy/images/{0}.png'>{0}</a> Score: {1}<br/>".format(r[0], score)

print '<p><a href="/bottsy/bottsy.py">Main Page</a></p>'

print '</html>'


