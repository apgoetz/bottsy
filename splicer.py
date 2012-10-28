#!/usr/bin/python2

from dbclient import *
import random
import gen_xc
import pickle
import copy


def splice():

	conn = init_db("bottsydb")
	EID = get_open_eid(conn) 
	setScore = 0
	for i in get_active_xc(conn, EID):
		setScore += i[6]
		
	for i in range(100):
		parent = select_xc(conn, xcid)
		xc = extract_xc(parent)
		child = mutatue(xc)
		add_xc(conn, EID, 1, child, "parents", 0, 0)
	

def select_xc(conn, EID):
	get_active_xc(conn, EID)
	
	

def extract_xc(parent):
	return pickle.loads(str(parent[3]))
	
def print_xc(xc):
		print xc[0]

		for i in xc[1]:
			print i

# grabs one portion of a chromosome
# and swaps it with another portion
# parent parameter is a tuple defined
# from the Chromosome structure
# defined above.
def transpose(xc, randNum):
	return None

	
# 
def cross(xc1, xc2):

	return None
	
def mutate(xc):

	child = copy.deepcopy(xc)

	threshold = random.randint(1,2)
	field = random.randint(1,8)
	move = random.randint(1,2)
	weight = random.randint(1,2)

	if (field == 8):
		move = {
			1: "line",
			2: "turn",
		} [move]

		weight = {
			1: "L",
			2: "T",
		} [weight]

	else:
		move = None
		weight = None
		randMin = {
			1: 0,
			2: 0,
			3: -360,
			4: -360,
			5: 100,
			6: 100,
			7: 0,
		} [field]
		randMax = {
			1: 500,
			2: 500,
			3: 360,
			4: 360,
			5: 20000,
			6: 20000,
			7: 254,
		} [field]

	threshold = {
		1: "light",
		2: "dark",
	} [threshold]

	field = {
		1: "dMax",
		2: "dMin",
		3: "phiMax",
		4: "phiMin",
		5: "rtMax",
		6: "rtMin",
		7: "lSense",
		8: "weights",
	} [field]
		
		
	# if it is a weighted value,
	if(field == "weights"):
		child[threshold][field][move][weight] = random.random()
		weight2 = {
			"L": "T",
			"T": "L",
		} [weight]
		child[threshold][field][move][weight2] = (1.0 - child[threshold][field][move][weight])
	else:
		child[threshold][field] = random.randint(randMin,randMax)
		
	print "%s %s %s %s" % (threshold, field, move, weight)

	return child



