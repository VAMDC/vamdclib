

The Request - Module
====================

About 
-------------


Library Classes and Methods
---------------------------------------------

.. automodule:: request
   :members:

Examples
--------

:: 

  >>> import request
  >>> req = request.Request()
  >>> req.setnode(cdms)
  >>> req.setquery("Select Species")
  >>> result = req.dorequest()

req contains now an instance of the Request class. The database CDMS is selected (see example in nodes.py) and a 
query which selects all species avaialable at the CDMS database is formulated. The last command performs the
request and returns an instance of results.Result which contains the return raw xml string and the data parsed
into dictionaries whose layout has been defined in spectmodel.py
