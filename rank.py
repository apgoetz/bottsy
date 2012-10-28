#!/usr/bin/python2
import cgi
from dbclient import *

conn = init_db('bottsydb')

eid = get_open_eid(conn)



print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print '<html>'
form = cgi.FieldStorage()
if "eid" not in form:
    print '<h1>Current Robot Ranking:</h1>'
else:
    eid = int(form['eid'].value)
    print '<h1> Robot Ranking for Generation %d </h1>' % eid

rows = get_ranked_xc(conn, eid).fetchall()
for r in rows:
    score = get_score(conn, r[0])
    print "<a href='/bottsy/show.py?id={0}'>{0}</a> Score: {1}<br/>".format(r[0], score)

print '<p><a href="/bottsy/bottsy.py">Main Page</a></p>'

print '</html>'


