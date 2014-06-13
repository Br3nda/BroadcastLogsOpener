#!/usr/bin/env python

import subprocess
import os

from elasticsearch import Elasticsearch
es = Elasticsearch()



def process_file(root, filename):
    full_filename = '{root}/{filename}'.format(root=root, filename=filename)
    print "PROCESSING ==== {filename}".format(filename=filename)
  
    if filename.lower().endswith('.doc') or filename.lower().endswith('.rtf'):
	contents = text_from_doc(full_filename)
    elif filename.lower().endswith('.txt'):
	return
	f = open(full_filename, 'r')
	contents = f.read()
	f.close()
    else:
	print "I don't know how to read this : " + filename
	return
  
    if not contents:
	print "I don't know how to read this"
	return
  
    try:
	contents = contents.decode("ascii","ignore")
    except:
	print "------------------------------"
	print contents
	raise
   
    assert contents
    
    print contents
    print "======================"
    
    body = {"filename": full_filename, 
	    #"contents": contents,
	    }
    if contents.find("PRESENTER:"):
	body['interview'] = interview_data(contents)
	
    print body
	
    try:
	print es.index(index="basic-index", doc_type="test-type", id=filename, body=body)
    except Exception, e:
	print contents
	raise

def interview_data(contents):
    lines = contents.split("\n")
    title = lines[0]
    return {'title': title}

def text_from_doc(full_filename):
    return subprocess.check_output(['catdoc', full_filename])


for root, dirs, files in os.walk('./dataset'):
    for filename in files:
	if filename.endswith('.doc'):
	    process_file(root, filename)

	
	
#process_file('MSDL-0428_problem files', 'LOG1127.txt')