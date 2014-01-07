# -*- coding: utf-8 -*-
import os
import re
import sys 
reload(sys) 
sys.setdefaultencoding('utf8')

class Entity:
	def __init__(self, id, offset, content):
		self.id = id
		self.offset = offset
		self.content = content

def init_input(id, dir):
	input = open(dir, "r")
	content = input.read()
	content = unicode(content, "utf8")
	strs = re.split("[0-9]+\.\n",content)
	offset = 0
	for string in strs:
		if offset != 0:
			entities.append(Entity(id, offset, string))
		offset += 1

def insert(entities):
	for entity in entities:
		entity.content = entity.content.replace("\n"," ")
		entity.content = entity.content.strip()
		question = entity.content[0:entity.content.find("A.")]
		question = question.strip()
		entity.question = question
		sentences.append(question)

def clear(entities):
	for entity in entities:
		entity.shortQuestion = trie_cut(entity.question, sentences, 10)
		entity.content = entity.content.replace(entity.question,"")
		if re.match("[\s\S]*[ABCDE]+$",entity.content) == None:
			print entity.content , entity.id, entity.offset
		entity.content = entity.content.strip()
		entity.answer = entity.content[len(entity.content)-1]
		entity.content = entity.content[0:-1].strip()
		entity.content = entity.content.replace("答案:","")
		entity.content = entity.content.strip()
		strs = re.split("[ABCDE]\.",entity.content)
		del strs[0]
		i = 0
		for str in strs:
			strs[i] = str.strip()
			i += 1
		s = strs[ord(entity.answer) - 65]
		entity.answer = trie_cut(s, strs, 2)
		# if entity.answer == None:
		# 	print entity.answer, entity.id, entity.offset
		result = "%s (%s-%s) %s" % (entity.shortQuestion, entity.id, entity.offset, entity.answer)
		results.append(result)

def trie_cut(string, strings, minLen):
	if (len(string) <= 1) :
		return string
	if minLen >= len(string):
		minLen = 1
	for i in range(minLen, len(string)+1):
		count = 0
		temp = string[0:i]
		for sentence in strings:
			if sentence.find(temp) == 0:
				count += 1
		if (count == 1):
			return temp

entities = []
sentences = []
results = []
path = "./data/"
for dir in os.listdir(path):
	if re.match(".*.txt", dir):
		id = dir.replace(".txt","")
		init_input(id, path + dir)
output = open("output.txt","w")
insert(entities)
clear(entities)

results.sort()
for result in results:
	print result
	output.write(result + "\n")
