#!/usr/bin/env python
import logging
import subprocess
import os
import time
import datetime
import dateutil.parser

logger = logging.getLogger('process')
logger.setLevel(logging.DEBUG)
h = logging.StreamHandler()
h.setLevel(logging.WARNING)
formatter = logging.Formatter('%(levelname)s - %(message)s')
h.setFormatter(formatter)
logger.addHandler(h)

from elasticsearch import Elasticsearch
es = Elasticsearch()


def get_content(full_filename):
    try:
	# WORD DOCS
	if filename.lower().endswith('.doc') or filename.lower().endswith('.rtf'):
	    return text_from_doc(full_filename)
	# Boring txt
	elif filename.lower().endswith('.txt'):	
	    f = open(full_filename, 'r')
	    contents = f.read()
	    f.close()
	    return contents
	elif filename.lower().endswith('.wpd'):
	    return text_from_wpd(full_filename)
	# TODO
	else:
	    logger.error( "I don't know how to read this : " + full_filename)
	    return
    except Exception, e:
	logger.error("Unable to read contents from {filename}".format(filename=full_filename))
	logger.error(e)
    

def process_file(root, filename):
    full_filename = '{root}/{filename}'.format(root=root, filename=filename)
    logger.info("PROCESSING ==== {filename}".format(filename=filename))
  
  
  
    contents = get_content(full_filename)
  
    if not contents:
	logger.error("I found no contents in this file: {filename}".format(filename=full_filename))
	return
  
    try:
	contents = contents.decode("ascii","ignore")
    except:
	logger.error("Error decoding file: " + filename)
	raise
   
    assert contents
    
    body = {"filename": full_filename, 
	    #"contents": contents,
	    }
    
    lines = contents.split("\n")
    if not contents:
        return
    elif lines[0].strip() == 'NEWZTEL MONITORING SERVICE':
        #print contents
        pass
    else:
        interview_data(contents, filename)

	
    try:
        logger.debug( es.index(index="newztel-index", doc_type="test-type", id=filename, body=body))
    except Exception, e:
        print contents
        raise

def get_date_from_line(line):
    original = line
    logger.debug(line)
    line = line.strip()
#     line = line.replace('.', ' ')
#     line = line.replace(',', ' ')
#     line = line.replace('  ', ' ')
#     
#     line = line.replace(' AUG ', ' AUGUST ')
#     line = line.replace(' NOV ', ' NOVEMBER ')

#     print line.split()
    date_string = ' '.join(line.split(" ")[-3:])
#     print '"' + date_string + '"'
    if not date_string:
        logger.warning("Cannot find a date. filename={filename} line={line}".format(line=line, filename=filename))
        logger.warning(original)
        return 
    logger.debug("Date = {date}".format(date=date_string))
    
    try:
        
        date = dateutil.parser.parse(date_string)
#         date = datetime.datetime.strptime(date_string, '%d %B %Y')
#     print date
        return date
    except ValueError, e:
        logger.error('Cannot get date from "{d}"'.format(d=date_string))
        logger.error(e)
        logger.warning(original)
        time.sleep(1)

    
def interview_data(contents, filename):
    lines = contents.split("\n")
    title = lines[0].strip()
    
    for i in range(0, len(lines)):
        if not title.strip():
            title = lines[i]
        else:
            break
        
    date = get_date_from_line(title)

    if not date:
        logger.warning('--------------- {filename} --------------------------'.format(filename=filename))
        for i in range(0, 7 if len(lines) >=7 else len(lines)):
            print "{i} {line}".format(line=lines[i], i=i)
        logger.warning('-----------------------------------------')
        print
        print
#         assert False
        return
        
    logger.debug("Title = {title}".format(title=title))
    
    body = {
    	    'title': title,
    	    'filename': filename,
    	    'date': date
    	    }
    
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

def text_from_wpd(full_filename):
    return subprocess.check_output(['wpd2text', full_filename])

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