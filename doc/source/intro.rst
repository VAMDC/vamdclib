
This document covers the **release 0.1** of the python library *vamdclib*.

Links to HTML-versions:

* Last release: http://
* Latest development: http://

Links to PDF-versions:

* Last release: http:// 
* Latest development: http://


.. _intro:

Introduction
=============

About VAMDC
-------------

The Virtual Atomic and Molecular Data Center is a EU FP7 research 
infrastructure project. A comprehensive documentation about the project,
standards and related software can be found on the official webpage http://vamdc.eu/.

About this library
------------------

This library contains several modules that implement access to VAMDC's infrastructure. 
It allows to query the central registry service to obtain information about registered
VAMDC database nodes and to send queries to these nodes as well as to process the retrieved
data. The data is made available as python dictionaries. Tools to store and manage the data 
in a local sqlite3 database or basex - xml database are included. 

