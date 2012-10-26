#!/usr/bin/python2
import os
import random
from math import *
from Tkinter import *

DEF_WIDTH = 2

def nextState(state):
	random.seed()
	weight = random.randint(0,4)
	stateArray = ('L', 'A', 'T', 'T', 'T')
	return stateArray[weight]
	
def boundaryAdjust(positionA, positionB, expectedA, expectedB, boundary):
	return (expectedB - ((abs(expectedA - boundary)*(expectedB - positionB))/(expectedA - positionA)))

def drawArc(x, y, vector, theta, r, cv):
	getStartAngle = (-90, 0, 90, 180)
	startAng = getStartAngle[random.randint(0,3)]
	
	if vector >= 0 & vector <= 45: startAng = 0
	elif vector > 45 & vector <= 90: startAng = 90
	elif vector > 90 & vector <= 180: startAng = 180
	elif vector > 180 & vector < 360: startAng = -90
	
	bbox = x, y, x, y
	xEnd = x 
	yEnd = y
	if (startAng == 0):
		# Movement A, E
		bbox = (x - 2*r), (y - r), (x), (y + r)
		adjTheta = theta
		xEnd = x - r*(1 - cos(radians(adjTheta)))

		yEnd = y - r*sin(radians(adjTheta))
	elif (startAng == 180):
		# Movement C, G
		bbox = (x), (y - r), (x + 2*r), (y + r)
		adjTheta = theta
		xEnd = x + r*(1 - cos(radians(adjTheta)))
		yEnd = y + r*(sin(radians(adjTheta))) 
	elif (startAng == 90):
		# Movement F, H
		bbox = (x - r), (y), (x + r), (y + 2*r)
		adjTheta = startAng + theta
		xEnd = x + r*cos(radians(adjTheta))
		yEnd = y + r*(1 - sin(radians(adjTheta)))
	elif (startAng == -90):
		# Movement B, D
		bbox = (x - r), (y - 2*r), (x + r), (y)
		adjTheta = (270 + theta)
		xEnd = x + r*(cos(radians(adjTheta)))
		yEnd = y - r*(1 + sin(radians(adjTheta)))	
	
	if xEnd > 500:
		yEnd = boundaryAdjust(x, y, xEnd, yEnd, 500)
		xEnd = 500
	if xEnd < 0: 
		yEnd = boundaryAdjust(x, y, xEnd, yEnd, 0)
		xEnd = 0
	if yEnd > 500: 
		xEnd = boundaryAdjust(y, x, yEnd, xEnd, 500)
		yEnd = 500
	if yEnd < 0: 
		xEnd = boundaryAdjust(y, x, yEnd, xEnd, 0)
		yEnd = 0
	
	cv.create_arc( bbox, width=DEF_WIDTH, start=startAng, extent=theta, style = ARC)
	
	return xEnd, yEnd

def drawLine(x, y, vector, d, cv):

	xEnd = x + (d * cos(radians(vector)))
	yEnd = y + (d * sin(radians(vector)))
	
	if xEnd > 500: xEnd = 500
	if xEnd < 0: xEnd = 0
		
	if yEnd > 500: yEnd = 500
	if yEnd < 0: yEnd = 0		
		
	cv.create_line( x, y, xEnd, yEnd, width=DEF_WIDTH)	
	
	return xEnd, yEnd

master = Tk()

print "Initializing canvas..."
cv = Canvas(master, width=500, height=500)
cv.pack()

i = 0

xl = {'rtMin':5000 , 'rtMax':10000, 'dMin':5, 'dMax':25, 'thetaMin':-70, 'thetaMax':70, 'rMin':5, 'rMax':25, 'phiMin':-45, 'phiMax':45} 

print "Initializing starting position..."

max_iter = random.randint(xl['rtMin'],xl['rtMax'])
position = 250, 250
vector = 0
state = 'L'

print "Generating Random line art..."

while i < max_iter:
	state = nextState(state)
	if state == 'L':
		d = random.randint(xl['dMin'],xl['dMax'])
		position = drawLine(position[0], position[1], vector, d, cv)
	elif state == 'A':
		theta = random.randint(xl['thetaMin'],xl['thetaMax'])
		r = random.randint(xl['rMin'],xl['rMax'])
		position = drawArc( position[0], position[1], vector, theta, r, cv)   
	elif state == 'T':
		# change direction
		vector += random.randint(xl['phiMin'],xl['phiMax'])
		if vector < -360: vector += 360
		if vector > 360: vector -= 360
	i = i + 1
	master.update()

print "Saving image file... "
cv.postscript(file = "output.eps")
print "Waiting to end..."
mainloop()
