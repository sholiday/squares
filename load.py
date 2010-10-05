#!/usr/bin/python
import sys
import beanstalkc
from datetime import datetime
import beanstalkc
import syslog
import time
import json
import uuid

length=int(sys.argv[1])

word_list = filter(lambda x: x.isalpha(), map(lambda x: x.strip(), open('wordlists/words_len_%s' % length).readlines()))
beanstalk = beanstalkc.Connection(host='corn-syrup.csclub.uwaterloo.ca', port=14711)

beanstalk.use('size-%s'%length)

message={}
for word in word_list:
	message['word']=word
	print word
	beanstalk.put(json.dumps(message, separators=(',',':')),ttr=600)
