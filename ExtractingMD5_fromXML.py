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
from xml.dom import minidom
from time import gmtime, strftime

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
	
	# XML parsing 
	xmldoc = minidom.parse(fn)
	files = xmldoc.getElementsByTagName('fileobject')
	
	# print csv head
	print "# Extracting from %s at %s" % (fn, strftime("%Y-%m-%d %H:%M:%S", gmtime()))
	print "# filename, MD5"
	
	# print extracted data
	for fileobject in files:
		fn = fileobject.getElementsByTagName("filename")[0]
		md5 = fileobject.getElementsByTagName("hashdigest")[0]
		print fn.firstChild.data +", "+ md5.firstChild.data

if __name__ == "__main__":
	main()
