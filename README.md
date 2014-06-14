BroadcastLogsOpener
===================

This was created at the Heritage Preserve hackfest, at NZ National Library, 2014-06-13.

 * Reads Newztel broadcast logs (varying file formats)
 * inserts the contents into an elastic search.
 * Parse facets from the text, e.g. date, speaker, source (e.g. RNZ)
 * escalates unexpected file contents to errors

This is proof of concept only.


Supported Formats
=================
* txt
* doc
* rtf
* wpd (some of them)

Requirements
============
Elastic search running on local host

How to see the data we indexed
==============================
I used the html ui here: http://mobz.github.io/elasticsearch-head/

What Next?
===========

We used elastic search, but the end goal is to send to DigitalNZ

Each file read has a "PID". There is a spreadsheet that maps the filename to the PID. A URL for each file can be calculated from the PID. 


