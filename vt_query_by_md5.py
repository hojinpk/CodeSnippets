#!/usr/bin/python
#-*- coding: utf-8 -*-
"""
Query to VirusTotal by MD5 in order to check result detected from AntiVirus VirusTotal has.

Usage:
 vt.py [OPTION(s)] PAHT
 -i --input          Specify a file including MD5
 -h --help           Display this help
 
Here is a sample for the result.

 C:\> vt_query_by_md5.py -i md5list.txt
 8e3e26957fde06590a7def9d1d4eecca,TheHacker,Trojan/Rbot
 a526b9e7c716b3489d8cc062fbce4005,Clean
 55272fe96ad87017755fd82f7928fda0,NOT
 55272fe96ad87-17755fd82f7928fda-,!MD5
"""
import sys
import os
import getopt
import urllib
import urllib2
import simplejson
import re

def vt_report(rsrc):
	url = "https://www.virustotal.com/api/get_file_report.json"
	parameters = {"resource": rsrc, "key" :"432e00a1d65de8631742affcff0117c8ec76cd200fabecfe7c89bc176d364542"}
	data = urllib.urlencode(parameters)
	req  = urllib2.Request(url, data)
	response = urllib2.urlopen(req)
	json = response.read()   
	return json

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
			file_path = a
		else:
			print __doc__
			sys.exit(0)
	
	fi = open(file_path, 'r')
	for line in fi:
		line = line.strip('\r\n')
		if len(line) > 32:
			md5 = line[:32]
			#path = line[34:]
			md5.upper()
			if re.match(r"[0-9a-f]{32}", md5) is None:
				print "%s,!MD5" % md5
				continue
			
			data = vt_report(md5)
			entry = simplejson.loads(data)
			
			if entry['result'] == 1:
				detected_cnt = 0
				# The file matched by the MD5 is exsited on VT
				for k, v in entry['report'][1].items():
					if len(v) > 0:
						detected_cnt += 1
						# MD5, AntiVirus, Result
						str = md5 +','+ k +','+ v
						print str
				if detected_cnt == 0:
					print "%s,Clean" % md5
			else:
				# The file matched by the md5 is not existed on VT
				str = md5 +','+ "NOT"
				print str

	fi.close()

if __name__ == "__main__":
	main()
