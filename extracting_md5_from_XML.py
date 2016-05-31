#!/usr/bin/python
#  -*- coding: utf-8 -*-
"""
Extract filename and MD5 from the XML file which was made by md5deep64.exe
Usage:
 vt.py [OPTION(s)] PAHT
 -i --input          a target file path
 -h --help           Display this help
"""
import sys
import os
import getopt
from time import gmtime, strftime
from bs4 import BeautifulSoup

def main():
	# parse command line options
	opts, args = getopt.getopt(sys.argv[1:], "hi:", ["help"])

	if len(opts) == 0:
		print __doc__
		sys.exit(0)
		
	# process options
	for op, a in opts:
		if op == '-h' :
			print __doc__
			sys.exit(0)
		elif op == '-i' :
			fn = a
			# print rsrc
		else:
			print __doc__
			sys.exit(0)

	# print csv head
	#print "# Extracting from %s at %s" % (fn, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	#print "# MD5, filename"
	
	# XML parsing 
	fp = open(fn, "r")
	soup = BeautifulSoup(fp, "xml")
	error_cnt = 0
	for node in soup.findAll('fileobject'):
		try:
			print "%s, %s" %(node.hashdigest.string,node.filename.string)
		except UnicodeEncodeError as e:
			#print(str(e))
			#print type(node.filename.string)
			#print type(node.hashdigest.string)
			error_cnt += 1
			pass
	#print "The End (ERR_CNT: %d)" % error_cnt

if __name__ == "__main__":
	main()
