#!/usr/bin/env python

# ========================================
# This script creates the initial database
# of microsatellites and the initial
# database of junctions using the output from
# the msat id program developed by Harshith 
# Chennamaneni (chenh@bu.edu)
# ========================================

import os
import MySQLdb							# database fuctions

# connect to database:
conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = "", db = "MSATS")
cursor = conn.cursor()

def is_tab_file(item):
	"""removes items from a list that don't end with '.out' """
	# this function is used in 'filter' command
	if item.endswith('.out') == True:
		return 1

def cleanuplocs(dirtystring):
	"""remove parenthesis and extraneous whitespace from line"""
	dirtystring = dirtystring.replace("(", "")
	dirtystring = dirtystring.replace(")", "")
	cleanstring = dirtystring.strip()
	return cleanstring
	
	
def create_table(genome):
	""" drops table if exists and creates an empty one for the supplied genome"""
	
	query = """DROP TABLE IF EXISTS """ + genome.upper() + """_MSATS"""
	
	cursor.execute(query)
	conn.commit() # required for inserting data!!
	
	query =  """CREATE TABLE """ + genome.upper() + """_MSATS (
	  `msat_id` int(11) NOT NULL auto_increment,
	  `organism` varchar(11) default NULL,
	  `fasta_id` varchar(100) default NULL,
	  `start_loc` int(11) default NULL,
	  `stop_loc` int(11) default NULL,
	  `type` varchar(11) default NULL,
	  `repeat_number` float(11) default NULL,
	  `repeat_seq` varchar(11) default NULL,
	  PRIMARY KEY  (`msat_id`),
	  KEY `start_loc` (`start_loc`)
	) ENGINE=InnoDB DEFAULT CHARSET=latin1"""
	
	cursor.execute(query)
	conn.commit() # required for inserting data!!
		

def all_msat_parse_infile(file_name,path,genome):
	""" parse output from tandem.java and add to db creating an appropriate msat table"""
	
	file_name = path+file_name			# create full path to file name (so script can be anywhere)
	infile = open(file_name,'r')		# open file
	
	count = 1		# count lines
	contig_id = ''
	for line in infile:
		if count % 100000 == 0: print "current count: ", count
		
		if line.startswith('>') == True:
			contig_id = line[1:]
			contig_id = contig_id.strip()
			continue
			
		line_words = line.split("\t")	# convert line into list on whitespace
		
		msat = line_words[0].upper()
		msat_start_loc = int(line_words[1])
		msat_len = int(line_words[2])
		
		# determine repeat type:
		msat_unit_len = len(msat)
		msat_type = ''
		
		msat_type_dict = {1:'mono', 2:'di', 3:'tri', 4:'tetra', 5:'penta', 6:'hexa', 7:'hepta', 8:'octa', 9:'nona', 10:'deca'}
		msat_type = msat_type_dict[msat_unit_len]
		msat_stop_loc = msat_start_loc + msat_len - 1  # need to subtract 1 from end to get the correct stopping position!!!
		msat_units = str(msat_len / msat_unit_len)
		msat_units = float(msat_units)
		
		query = """insert into """ + genome.upper() + """_MSATS (organism, fasta_id, start_loc, stop_loc, type, repeat_seq, repeat_number) VALUES (%s,%s,%s,%s,%s,%s,%s)"""
		
		# insert data into database:
		cursor.execute(query, (genome, contig_id, msat_start_loc, msat_stop_loc, msat_type, msat, msat_units))
		conn.commit() # required for inserting data!!
		
		count += 1		# update count of rows

def main():
	#'apiMel3'
	genomes = ['anoCar1']
	
	for genome in genomes: 
		create_table(genome)
	
	for genome in genomes: 
		path = "/Users/nick/Desktop/Projects/Benson - MSATS/Chen Scans/"+genome+"/"			# path to output
		print path
		dirList=os.listdir(path)								# get list of files in directory (e.g. directory containing chromosomes)
		dirList = filter(is_tab_file,dirList)					# filter out files not starting with 'All'
		print dirList
		for file_name in dirList:
			print file_name
			all_msat_parse_infile(file_name, path, genome)

main()	# call main function

# close down db connection:
cursor.close()
conn.close()

