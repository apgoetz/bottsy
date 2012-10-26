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


# dump all of the chromosome in the table to std out
def list_xc(conn):
    # get 'cursor'
    c = conn.cursor()
    for row in c.execute('SELECT * FROM chromosome'):
        print row
  
# list all chromosomes that match a specific experiment
def list_by_exp(conn, eid):
    #get 'cursor'
    c = conn.cursor()
    for row in c.execute('SELECT * FROM chromosome WHERE eid = %s' % eid):
        print row

# list all of the experiments in the database
def list_exp(conn):
    # get 'cursor'
    c = conn.cursor()
    for row in c.execute('SELECT * FROM experiment'):
        print row

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

# Set the alive state of a chromosome
def set_alive(conn, id, isalive):
    alive_val = 1 if isalive else 0
    conn.execute('UPDATE chromosome SET alive = %d WHERE id = %d' %(isalive, id))

def set_score(conn, id, score):
    conn.execute('UPDATE chromosome SET score = %f WHERE id = %f' %(float(score), id))

def set_age(conn, id, age):
    conn.execute('UPDATE chromosome SET age = %d WHERE id = %d' %(age, id))


    
    
def init_db(name):
####START OF SCRIPT


#Get the name of the database file to use

	dbname = name

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







