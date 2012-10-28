#!/usr/bin/python2
import os
import random
import pickle
import Image,ImageDraw

from math import *
from dbclient import *

DEF_WIDTH = 2 

def nextState(state, weightSet):
	if (state == 'L'):
		weights = weightSet['line']
	elif (state == 'A'):
		weights = weightSet['arc']
	elif (state == 'T'): 
		weights = weightSet['turn']
	stateSet = ('L','T')
	rnd = random.random() * sum(dict.values(weights))
	for i, w in enumerate(dict.values(weights)):
		rnd -= w
		if rnd < 0:
			return stateSet[i]
	
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
	
	if xEnd > 495:
		yEnd = boundaryAdjust(x, y, xEnd, yEnd, 495)
		xEnd = 495
	if xEnd < 5: 
		yEnd = boundaryAdjust(x, y, xEnd, yEnd, 5)
		xEnd = 5
	if yEnd > 495: 
		xEnd = boundaryAdjust(y, x, yEnd, xEnd, 495)
		yEnd = 495
	if yEnd < 5: 
		xEnd = boundaryAdjust(y, x, yEnd, xEnd, 5)
		yEnd = 5
	
	bbox = int(bbox[0]),int(bbox[1]),int(bbox[2]),int(bbox[3])
		
	cv.arc(bbox, startAng, theta, fill=0)
	
	return xEnd, yEnd

def drawLine(x, y, vector, d, cv):

	xEnd = x + (d * cos(radians(vector)))
	yEnd = y + (d * sin(radians(vector)))
	
	if xEnd > 495: xEnd = 495
	if xEnd < 5: xEnd = 5
		
	if yEnd > 495: yEnd = 495
	if yEnd < 5: yEnd = 5		
		
	cv.line( (x, y, xEnd, yEnd), fill=0, width=DEF_WIDTH)	
	
	return xEnd, yEnd

# check for xcid arg
if len(sys.argv) < 2:
	sys.exit()

xcid = sys.argv[1]

if os.path.exists("images/%s.png" % xcid):
	sys.exit()

#print "Openeing db"
conn = init_db("bottsydb")

#print "Loading xc"
xc_full = select_xc(conn,xcid)[3]
xc_full = pickle.loads(str(xc_full))
close_db(conn)

#print "Preparing blank image"
random.seed()
im = Image.open('blank.png')
cv = ImageDraw.Draw(im)

#print "Initializing starting position..."
i = 0
max_iter = random.randint(xc_full['light']['rtMin'],xc_full['light']['rtMax'])
position = 250, 250
vector = 0
state = 'L'
lightLevel = 0 
lSense = xc_full['light']['lSense']
ir_rad = 3

#print "Generating Random line art..."
while i < max_iter:
	
	for x in range(-ir_rad,ir_rad+1):
		for y in range(-ir_rad,ir_rad+1):
			lightLevel += im.getpixel((position[0] + x, position[1] + y))[0]
	lightLevel = lightLevel/(ir_rad * ir_rad)

	if (lightLevel > lSense): 
		xc = xc_full['light']
	else: 
		xc = xc_full['dark']
	lSense = xc['lSense']

	state = nextState(state,xc['weights'])
	if state == 'L':
		d = random.randint(xc['dMin'],xc['dMax'])
		position = drawLine(position[0], position[1], vector, d, cv)
	elif state == 'A':
		theta = random.randint(xc['thetaMin'],xc['thetaMax'])
		r = random.randint(xc['rMin'],xc['rMax'])
		position = drawArc( position[0], position[1], vector, theta, r, cv)   
	elif state == 'T':
		# change direction
		vector += random.randint(xc['phiMin'],xc['phiMax'])
		if vector < -360: vector += 360
		if vector > 360: vector -= 360
	i = i + 1

#print "Saving image file... "
im.save('images/%s.png' % xcid)
#print "Ending..."
