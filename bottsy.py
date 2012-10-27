#!/usr/bin/env python2

import cgi
import random

def random_line():
    afile = open('linuxwords')
    line = next(afile)
    for num, aline in enumerate(afile):
        if random.randrange(num + 2): continue
        line = aline
    return line.rstrip()

def display_pair():
    thing1 = random_line();
    thing2 = random_line();
    print "<h1>Click on the better thing:</h1>"
    print "<p><a href='test.py?winner="+thing1+"&loser="+thing2+"'>"+thing1+"</a>"
    print " or "
    print "<a href='test.py?winner="+thing2+"&loser="+thing1+"'>"+thing2+"</a></p>"
    


print "Content-Type: text/html"     # HTML is following
print                               # blank line, end of headers

form = cgi.FieldStorage()
print "<html>"
if "winner" not in form and "loser" not in form:
    print ""
else:
    
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

display_pair()

print "</html>"


