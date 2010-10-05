#!/usr/bin/python
import sys
import beanstalkc
from datetime import datetime
import beanstalkc
import time
import json
import uuid

length=int(sys.argv[1])
instance_name=sys.argv[2]
instance_id='id-%s'%uuid.uuid4()

word_list = filter(lambda x: x.isalpha(), map(lambda x: x.strip(), open('wordlists/words_len_%s' % length).readlines()))
word_dict = {}

logfile = open('squares_'+sys.argv[1]+'_'+instance_name+'_'+instance_id+'.log', 'a',0)
ans = open('squares_'+sys.argv[1]+'_'+instance_name+'_'+instance_id+'.ans', 'a',0)
	

def try_word(word):
	grid_e=list()
	for i in range(length):
		grid_e.append(list())
		for j in range(length):
			grid_e[i].append(' ')
	for i in range(length):
		grid_e[i][0]=grid_e[0][i]=word[i]
	run(grid_e,1)

def run(grid, row):
	pre=''
	for i in range(row):
		pre += grid[row][i]
	if word_dict.has_key(pre):
		for word in word_dict[pre]:
			for i in range(length):
				grid[i][row]=word[i]
				grid[row][i]=word[i]
			
			if (row==length-1):
				out= formatGrid(grid)
				log(31,'##SOLVED##\n'+out)
				ans.write(out)
				print out
			else:
				#check if this word has prefixes throughout the space
				goodWord=True
				for i in range(row,length):
					prefix=''
					for j in range(row+1):
						prefix+=grid[i][j]
					if not word_dict.has_key(prefix):
						goodWord=False
				if goodWord==True: 
					run(grid,row+1)
def formatGrid(grid):
	out='-------------------------\n'
	for row in grid:
		out +='|' + '|'.join(row) + '|\n'
	return out

#### The Actual Program

for word in word_list:
	for i in range(length):
 		substr = word[:i]
 		if not word_dict.has_key(substr):
			word_dict[substr] = list()
		word_dict[substr].append(word)
	
print 'Connecting to beanstalkd'
beanstalk = beanstalkc.Connection(host='corn-syrup.csclub.uwaterloo.ca', port=14711)

beanstalk.watch('size-%s'%length)
beanstalk.ignore('default')
beanstalk.use('log-%s'%length)

def log(level,message):
	formatted= '%s#L%s: %s' % (datetime.time(datetime.now()), level, message)
	logfile.write(formatted)
	print formatted
	if level > 19:
		info={}
		info['time']='%s'%datetime.time(datetime.now())
		info['level']=level
		info['message']=message
		info['instance_id']=instance_id
		info['version']='3_2'
		info['instance_name']=instance_name
		beanstalk.put(json.dumps(info, separators=(',',':')),ttr=10)

while (True):
	try:
		log(10,'Reserving a Job')
		job = beanstalk.reserve()
		log(10,'Got a job! JID:%s' % job.jid)
		message= json.loads(job.body)
		word=message['word']
		log(20,'Working on word <%s>' % word)
	
		try_word(word)
	
		log(20,'Finished word <%s>' % word)
		log(10,'Finished JID:%s, deleting' % job.jid)
		try:
			job.delete()
		except beanstalkc.CommandFailed:
			log(29,'Tried to delete job, perhaps we ran over time. <jid:%s>'%job.jid)
	except beanstalkc.DeadlineSoon:
		job.release()
