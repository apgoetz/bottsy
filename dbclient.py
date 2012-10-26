#!/usr/bin/python2

import sqlite3
import sys


def print_help():
    print '''
dbclient.py Usage:

dbclient.py [database] lx - List All Chromosomes
dbclient.py [database] le - List All Experiments
dbclient.py [database] lxe [eid] - List All Chromosomes from experiment eid
dbclient.py [database] ae [name] [heuristics] - add experimment
dbclient.py [database] ax [eid] [alive] [xc] [parents] [age] [score] add chromosome
'''

# list chromosome by id
def select_xc(conn, xcid):
	conn.row_factory = sqlite3.Row
	c = conn.cursor()
	c.execute('SELECT * FROM chromosome WHERE id = %s' % xcid)
	return c.fetchone()

# dump all of the chromosome in the table to std out
def list_xc(conn):
    # get 'cursor'
    c = conn.cursor()
    return c.execute('SELECT * FROM chromosome')
  
# list all chromosomes that match a specific experiment
def list_by_exp(conn, eid):
	#get 'cursor'
	c = conn.cursor()
	return conn.execute('SELECT * FROM chromosome WHERE eid = %s' % eid)

def list_exp(conn):
    # get 'cursor'
    c = conn.cursor()
    return c.execute('SELECT * FROM experiment')

# add an experiment to the db
def add_exp(conn, name, heuristics):
    #get 'cursor'
    c = conn.cursor()
    c.execute('INSERT INTO experiment (name, heuristics) VALUES ("%s", "%s")' % (name, heuristics))

def add_xc(conn, eid, alive, xc, parents, age, score):
    # get 'cursor'
    c = conn.cursor()
    c.execute(('INSERT INTO chromosome (eid, alive, xc, parents, age, score) VALUES' + 
              '("%s", %d, "%s", "%s", %d, %f)' % 
               (eid, int(alive), xc, parents, int(age), float(score))))

def init_db(dbname):
####START OF SCRIPT
	#make a connection to the database
	conn = sqlite3.connect(dbname)
	#once we have a connection we need a 'cursor' to actually do anything..
	c = conn.cursor()

	# first of all we need to capture the schema available for the
	# database. There are two main tables:
	#
	# experiment: contains metadata about the experiment being executed
	# +------------------------+-----------+-----------------+
	# | id INTEGER PRIMARY KEY | name TEXT | heuristics BLOB |
	# +------------------------+-----------+-----------------+
	c.execute('''CREATE TABLE IF NOT EXISTS experiment 
	(id INTEGER PRIMARY KEY,
	name TEXT NOT NULL,
	heuristics BLOB NOT NULL)''')

	# chromosomes: table about each chromosome
	# +------------------------+----------------------+---------------+---------+--------------+-------------+------------+
	# | id INTEGER PRIMARY KEY | eid INTEGER NOT NULL | alive BOOLEAN | xc BLOB | parents BLOB | age INTEGER | score REAL |
	# +------------------------+- --------------------+---------------+---------+--------------+-------------+------------+
	c.execute('''CREATE TABLE IF NOT EXISTS chromosome
	(id INTEGER PRIMARY KEY,
	eid INTEGER NOT NULL,
	alive BOOLEAN NOT NULL,
	xc BLOB NOT NULL,
	parents BLOB,
	age INTEGER NOT NULL,
	score REAL NOT NULL,
	FOREIGN KEY(eid) REFERENCES experiment(id))''')
	
	return conn

def close_db(conn): 
# close the db:
	conn.commit()
	conn.close()







