#!/usr/bin/python

word_list = filter(lambda x: x.isalpha(), map(lambda x: x.strip(), open('noapos').readlines()))
word_dict = {}
for x in xrange(1,50):
	word_dict[x] = set()

for word in word_list:
	word_dict[len(word)].add(word)

for len,words in word_dict.iteritems():
	out_file = open('words_len_%s' % len,'w')
	out_file.write('\n'.join(sorted(words)))
	out_file.write('\n')
	out_file.close()
