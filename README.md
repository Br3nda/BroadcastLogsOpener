BroadcastLogsOpener
===================

This was created at the Heritage Preserve hackfest, at NZ National Library, 2014-06-13.

This reads Newztel broadcast logs, and puts the contents into an elastic search engine.
This is proof of concept only.


Supported Formats
=================
* txt
* doc
* rtf

in progress: wpd (Corel/WP)


What Next?
===========
TODO: Parse facets from the text, e.g. date, speaker, source (e.g. RNZ)

We used elastic search, but the end goal is to send to DigitalNZ
Each file read has a "PID". There is a spreadsheet that maps the filename to the PID. A URL for each file can be calculated from the PID. 
Once we have facets, and a URL for each file, we can start to send to Digital NZ instead.

