#!/usr/bin/python2
import cgi
from dbclient import *
import pickle

conn = init_db('bottsydb')
xcid = 2

print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

print '<html>'

form = cgi.FieldStorage()
if "xcid" not in form:
    print '<h1>Show Art:</h1>'
else:
    xcid = int(form['id'].value)

xc = pickle.loads(str(select_xc(conn,xcid)[3]))
print '<h1>Show Art and xc:</h1>'

score = get_score(conn, xcid)
print "<img src='/bottsy/images/{0}.png'> <br/>Score: {1}<br/>xc: {2}".format(xcid, int(score), xc)

print '<p><a href="/bottsy/bottsy.py">Main Page</a></p>'

print '</html>'


