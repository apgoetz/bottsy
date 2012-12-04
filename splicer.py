#!/usr/bin/python2

from dbclient import *
import random

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
	
def get_weighted_id(conn, EID):
	rows = get_active_xc(conn,EID)
	xc_data = map(lambda r: select_xc(conn, r[0]), rows)
	random.shuffle(xc_data)
	ranks = map(lambda r: r[6], xc_data)
	rnd = random.random() * sum(ranks)
	for i, w in enumerate(ranks):
		rnd -= w
		if rnd < 0:
		        return xc_data[i]
	
	

def extract_xc(parent):
	return pickle.loads(str(parent[3]))
	
def print_xc(xc):
		print xc[0]

		for i in xc[1]:
			print i

# grabs one portion of a chromosome
# and swaps it with another portion
def transpose(xc):
	selection1 = rand_selection()
	selection2 = rand_selection()
	
	return None

	
# 
def cross(xc1, xc2):
	child = copy.deepcopy(xc1)
	child['light'] = xc2['dark']
	return child

	
def mutate(xc):

	child = copy.deepcopy(xc)

	selection = rand_selection()
	
	threshold = selection[0]
	field = selection[1]
	move = selection[2]
	weight = selection[3]

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
		
#	print "%s %s %s %s" % (threshold, field, move, weight)

	return child



def get_mutated_xc(conn, eid):
	xc_row1 = get_weighted_id(conn,eid)
	xc_row2 = get_weighted_id(conn,eid)
	#print 'chosen id = %d' % xc_row[0]
	return mutate(cross(extract_xc(xc_row1),extract_xc(xc_row2)))


# returns a tuple of the following format:
# (threshold, field, move, weight)
# NOTE: if field is not of type "weight",
# both move and weight will be empty (None)
def rand_selection():
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
		# define what the maximum/minimum random value will be
		# based on what was chosen
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

	# Map numbers to threshold type
	threshold = {
		1: "light",
		2: "dark",
	} [threshold]

	# Map number to field type
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

return (threshold, field, move, weight)

