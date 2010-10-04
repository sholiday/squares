#!/usr/bin/python
import sys
from datetime import datetime

length=int(sys.argv[1])

word_list = filter(lambda x: x.isalpha(), map(lambda x: x.strip(), open('words_len_%s' % length).readlines()))
word_dict = {}

log = open('sq_'+sys.argv[1]+'_'+sys.argv[2]+'.log', 'a',0)
ans = open('sq_'+sys.argv[1]+'_'+sys.argv[2]+'.ans', 'a',0)

def run(grid, row):
	#print row
        if row==length:
		print '### SOLVED'
                out= formatGrid(grid)
		log.write(out)
		ans.write(out)
		print out
	else:
                pre=''
                for i in range(row):
                        pre += grid[row][i]

                if word_dict.has_key(pre):
                        for word in word_dict[pre]:
                                for i in range(length):
                                        grid[i][row]=word[i]
					grid[row][i]=word[i]
				run(grid,row+1)
def formatGrid(grid):
	#print grid
	out='-------------------------\n'
	for row in grid:
		out +='|' + '|'.join(row) + '|\n'
	return out

for word in word_list:
        for i in range(length):
                substr = word[:i]
                if not word_dict.has_key(substr):
                        word_dict[substr] = list()
                word_dict[substr].append(word)

if (sys.argv[2] == 'all'):
	words=word_list
else:
	words=word_dict[sys.argv[2]]

for word in words:
	t=datetime.time(datetime.now())
        out = '%s: Trying %s' % (t,word)
        log.write(out+'\n')
	print out
	grid_e=list()
        for i in range(length):
                grid_e.append(list())
                for j in range(length):
                        grid_e[i].append(' ')
	for i in range(length):
		grid_e[i][0]=grid_e[0][i]=word[i]
	run(grid_e,1)
