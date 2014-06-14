#!/usr/bin/env python
import logging
import subprocess
import os
import time
import datetime

logger = logging.getLogger('process')
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)

from elasticsearch import Elasticsearch
es = Elasticsearch()



def process_file(root, filename):
    full_filename = '{root}/{filename}'.format(root=root, filename=filename)
    logger.debug("PROCESSING ==== {filename}".format(filename=filename))
  
  
    # WORD DOCS
    if filename.lower().endswith('.doc') or filename.lower().endswith('.rtf'):
	contents = text_from_doc(full_filename)
    # Boring txt
    elif filename.lower().endswith('.txt'):	
	f = open(full_filename, 'r')
	contents = f.read()
	f.close()
    # TODO
    else:
	logger.error( "I don't know how to read this : " + full_filename)
	return
  
    if not contents:
	logger.error("I found no contents in this file:" + full_filename)
	return
  
    try:
	contents = contents.decode("ascii","ignore")
    except:
	logger.error("Error decoding file: " + filename)
	raise
   
    assert contents
    
    #print contents
    #print "======================"
    
    body = {"filename": full_filename, 
	    #"contents": contents,
	    }
    if contents.find("PRESENTER:"):
	interview_data(contents, filename)
	
    logger.info(body)
	
    try:
	logger.debug( es.index(index="newztel-index", doc_type="test-type", id=filename, body=body))
    except Exception, e:
	print contents
	raise

def interview_data(contents, filename):
    lines = contents.split("\n")
    title = lines[0]
    logger.debug("Title = {title}".format(title=title))
    
    body = {
		    'title': title,
		    'filename': filename,
		    
		    }
    try:
	date = title.split("\t")[1]
	logger.debug("Date = {date}".format(date=date))

	body['date'] = datetime.datetime.strptime(date, '%A %d %B %Y')
    except:
	pass
    
    dialogue = []
    prev_line = None
    speaker = None
    paragraph = ''
    line_no = 0
    
    for line in lines:
	logger.debug("-----------------------------------------------")
	logger.debug("line = " + line)
	paragraph += ' ' + line
	logger.debug("-----------------------------------------------")
	logger.debug(paragraph)
	
	if prev_line == '':
	    if not speaker and line.find(':') != -1:
		speaker = line.split(':')[0]
		logger.debug("Speaker = {speaker}".format(speaker=speaker))
	    else:
		speaker = ''
	
	if line == '':
	    #print "**gap"
	    if speaker and paragraph:
		body['speaker'] = speaker
		body['statement'] = paragraph
		
		item_id= '{filename}.dialogue.{line_no}'.format(filename=filename, line_no=line_no)
		 #body
		es.index(index='speaker-index', doc_type='speaker', id=item_id, body=body)
		paragraph = ''
		speaker = ''
	      
	   
	prev_line = line
	line_no += 1
	#time.sleep(0.5)

    return {'title': title} #, dialogue: dialogue}

def text_from_doc(full_filename):
    return subprocess.check_output(['catdoc', full_filename])


try:
    es.indices.delete(index='speaker-index')
    #es.indices.delete(index='interview-index')
    #es.indices.delete(index='basic-index')
except:
    pass

for root, dirs, files in os.walk('./dataset'):
    for filename in files:
	process_file(root, filename)

	
	
##process_file('MSDL-0428_problem files', 'LOG1127.txt')