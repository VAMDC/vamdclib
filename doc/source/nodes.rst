The Node - Module
=================

About
---------------------

Information about registered VAMDC nodes are stored in the VAMDC registry service.
The registry contains a list of all registered database nodes and their url's. 

More information on the VAMDC registry service can be found in the documentation for
the VAMDC standards: http://www.vamdc.eu/documents/standards/registry/ 


Library Classes and Methods
---------------------------------------------

.. automodule:: nodes
   :members:

Example:
--------

The following example shows how to get an node instance for CDMS::

  >>> import nodes
  >>> nl = nodes.Nodelist()
  >>> cdms = nl.getnode('ivo://vamdc/cdms/vamdc-tap-dev')
  >>> cdms.url
  u'http://cdms.ph1.uni-koeln.de/cdms/tap/'

The 'getnode' method can be replaced by findnode if the 'searchstring' is unique::

  >>> nl.findnode ('CDMS')


