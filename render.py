import random
import math
from Tkinter import *

master = Tk()

print "Initializing canvas..."
cv = Canvas(master, width=500, height=500)
cv.pack()

i = 0
state = 'L'
xl = {'rtMin':5000 , 'rtMax':10000, 'dMin':5, 'dMax':25, 'thetaMin':0, 'thetaMax':360, 'rMin':5, 'rMax':25, 'phiMin':0, 'phiMax':360} 
delta = (0,0)
direction = (0,0)

print "Initializing starting position..."
x2 = random.randint(0,500)
y2 = random.randint(0,500)

print "Generating Random line art..."
max_iter = random.randint(xl['rtMin'],xl['rtMax'])
while i < max_iter:
	x1 = x2
	y1 = y2

	state = nextState(state)
	if state == 'L':
		delta = init_line(xl['dMin'],xl['dMax'])
		x2 += delta[0]*direction[0]
		y2 += delta[1]*direction[1]
		cv.draw_line(x1,y1,x2,y2, width = defWidth)
	elif state == 'A':
		delta = init_arc(xl['thetaMin'],xl['thetaMax'],xl['rMin'],xl['rMax'])
		x2 += delta[0]*direction[0]
		y2 += delta[1]*direction[1]
		cv.draw_arc(x1,y1,x2,y2, width = defWidth, style = ARC)
	elif state == 'T':
		# change direction
		direction = rotate(xl['phiMin'],xl['phiMax'])
		break

	theta = random.randint(0,360)
	r = random.randint(0,random.randint(0,25))
	x2 += int(r * math.cos(theta))
	y2 += int(r * math.sin(theta))
 	print "Coordinates: ", x2, y2

#	test = random.randint(0,3)
#	if (test == 0):
#		x2 += random.randint(0,random.randint(0,15))
#		y2 += random.randint(0,random.randint(0,15))
#	elif (test == 1):
#		x2 -= random.randint(0,random.randint(0,15))
#		y2 -= random.randint(0,random.randint(0,15))
#	elif (test == 2):
#		x2 += random.randint(0,random.randint(0,15))
#		y2 -= random.randint(0,random.randint(0,15))
#	else:
#		x2 -= random.randint(0,random.randint(0,15))
#		y2 += random.randint(0,random.randint(0,15))
	if x2 > 500:
		x2 = 500
	if y2 > 500:
		y2 = 500
	if x2 < 0:
		x2 = 0
	if y2 < 0:
		y2 = 0		
	cv.create_line( x1, y1, x2, y2, width=3)	
	i = i + 1

	master.update()
print "Saving image file... "
cv.postscript(file = "output.eps")
print "Waiting to end..."
mainloop()
