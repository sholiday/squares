#!/usr/bin/python
import sys
import beanstalkc
from datetime import datetime
import beanstalkc
import syslog
import time
import json
import uuid

beanstalk = beanstalkc.Connection(host='corn-syrup.csclub.uwaterloo.ca', port=14711)
beanstalk.watch('log-'+sys.argv[1])
logfile = open('squares_logger_'+sys.argv[1]+'.log', 'a',0)

while (True):
	try:
		job = beanstalk.reserve()
		#message= json.loads(job.body)
		print job.body
		logfile.write(job.body+'\n')
		job.delete()
	except beanstalkc.DeadlineSoon:
		job.release()