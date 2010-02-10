#!/usr/bin/env python
# encoding: utf-8
"""
untitled.py

Created by Nicholas Crawford on 2009-10-14.
Copyright (c) 2009 Boston Univeristy. All rights reserved.
"""

import sys
import os
import MySQLdb		# database fuctions
import bx.seq.twobit

# connect to database:
conn = MySQLdb.connect(host = "localhost", user = "nick", passwd = "", db = "MSATS")
cursor = conn.cursor()

query = """select M.type, M.repeat_number, M.repeat_seq, M.fasta_id, M.start_loc, M.stop_loc
from ANOCAR1_MSATS M
where M.repeat_number > 8 and M.type = 'tri'"""

# ORDER BY RAND()

cursor.execute(query)

# setup twobit:
twobit_path = '/Users/nick/Desktop/Genomes/anoCar1/anoCar1.2bit'
t = bx.seq.twobit.TwoBitFile(file(twobit_path))

#seq = t['contig_8'][10:100]
flank = 800
fout = open('tri_msat_gtr8_repeats_800bpflank_anoCar1.fa','w')

for count, item in enumerate(cursor):
	msat_type, repeat_number, repeat_seq, scaffold_id, start_loc, stop_loc = item
	msat = t[scaffold_id][start_loc:stop_loc]
	seq = t[scaffold_id][start_loc-flank:stop_loc+flank]
	fout.write('>%s_%s_%s_%s_%s_%s\n' % (scaffold_id, start_loc, stop_loc, msat_type, repeat_seq, repeat_number))
	fout.write(seq+'\n')
	if count % 10000 == 0: print count


def main():
	pass


if __name__ == '__main__':
	main()

