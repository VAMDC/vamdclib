# -*- coding: utf-8 -*-
"""
This module defines classes which define and perform requests to individual VAMDC database nodes. An instance of type result.Result is returned
if a request has been performed.
"""

import sys
import os

try:
    from lxml import objectify
    is_available_xml_objectify = True
except ImportError:
    is_available_xml_objectify = False
 
from xml.etree import ElementTree

if sys.version_info[0] == 3:
    import urllib.parse
    urllib2 = urllib.parse
    from urllib.parse import urlparse
    from http.client import HTTPConnection, urlsplit, HTTPException, socket
    unicode = str
else:
    from urlparse import urlparse
    import urllib2
    from httplib import HTTPConnection, urlsplit, HTTPException, socket

if sys.version_info[0] == 3:
    from .settings import *
    from . import query as q
    from . import results as r
    from . import nodes
else:
    from settings import *
    import query as q
    import results as r
    import nodes


from dateutil.parser import parse

XSD = "http://vamdc.org/xml/xsams/1.0"

class TimeOutError(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, 408, "Timeout")
        self.strerror = "Timeout"

class NoContentError(Exception):
    def __init__(self, expr):
        self.expr = expr
        self.msg = "No content to perform operation on"
        
class Request(object):
    """
    A Request instance represents one request to a specified VAMDC database node. 
    """
    def __init__(self, node = None, query = None):
        """
        Initialize a request instance. 

        node: Database-Node to which the request will be sent
        query: Query which will be performed on the database.
        """
        self.status = 0
        self.reason = "INIT"
        self.baseurl = None

        if node != None:
            self.setnode(node)
            
        if query != None:
            self.setquery(query)

    def setnode(self, node):
        """
        Sets the node to which the request will be sent. If the node has not been specified already during the
        initialization of the instance, it has to be specified before the request will be performed in order to 
        obtain the Base-Url of the database node. Alternatively, the Base-Url can be set directly with the method 'setbaseurl'
        """
        self.status = 0
        self.reason = "INIT"

        try:
            self.node = node
            
            if not hasattr(self.node,'url') or len(self.node.url)==0:
                #print("Warning: Url of this node is empty!")
                pass
            else:
                self.baseurl = self.node.url
                if self.baseurl[-1]=='/':
                    self.baseurl+='sync?'
                else:
                    self.baseurl+='/sync?'
        except:
            print("There was a problem setting the node (%s)" % node)
            raise

    def setbaseurl(self, baseurl):
        """
        Sets the Base-Url to which the query will be sent. Usually this method is called internally via the method 'setnode' and
        is only called if requests shall be sent to nodes which are not registered in the VAMDC registry.
        
        """
        self.baseurl = baseurl
        if self.baseurl[-1]=='/':
            self.baseurl+='sync?'
        else:
            self.baseurl+='/sync?'

    def setquery(self, query):
        """
        Sets the query which shall be defined on the database node. Query could ether be a query.Query instance
        or a string. The query has to be specified before the request can be performed.
        """
        self.status = 0
        self.reason = "INIT"
        
        if type(query)==q.Query:
            self.query = query
            self.__setquerypath()
        elif type(query) == str or type(query) == unicode:
            self.query = q.Query(Query = query)
            self.__setquerypath()
        else:
            #print(type(query))
            #print("Warning: this is not a query object")
            pass
        

    def __setquerypath(self):
        """
        Sets the querypath which is appended to the nodes 'base'-url.
        """
        self.querypath = "REQUEST=%s&LANG=%s&FORMAT=%s&QUERY=%s" % ( self.query.Request,
                                                                     self.query.Lang,
                                                                     self.query.Format,
                                                                     urllib2.quote(self.query.Query))
        

    def dorequest(self, timeout = TIMEOUT, HttpMethod = "POST", parsexsams = True):
        """
        Sends the request to the database node and returns a result.Result instance. The
        request uses 'POST' requests by default. If the request fails or if stated in the parameter 'HttpMethod',
        'GET' requests will be performed. 
        The returned result will be parsed by default and the model defined in 'specmodel' will be populated by default 
        (parseexams = True).
        """
        self.xml = None
        #self.get_xml(self.Source.Requesturl)
        url = self.baseurl + self.querypath
        urlobj = urlsplit(url)
        
        conn = HTTPConnection(urlobj.netloc, timeout = timeout)
        conn.putrequest(HttpMethod, urlobj.path+"?"+urlobj.query)
        conn.endheaders()
        
        try:
            res = conn.getresponse()
        except socket.timeout:
            # error handling has to be included
            self.status = 408
            self.reason = "Socket timeout"
            raise TimeOutError

        self.status = res.status
        self.reason = res.reason

        if not parsexsams:
            if res.status == 200:
                result = r.Result()
                result.Content = res.read()
            elif res.status == 400 and HttpMethod == 'POST':
                # Try to use http-method: GET
                result = self.dorequest( HttpMethod = 'GET', parsexsams = parsexsams)
            else:
                result = None
        else:
            if res.status == 200:
                self.xml = res.read()

                result = r.Result()
                result.Xml = self.xml
                result.populate_model()
            elif res.status == 400 and HttpMethod == 'POST':
                # Try to use http-method: GET
                result = self.dorequest( HttpMethod = 'GET', parsexsams = parsexsams)
            else:
                result = None

        return result

    def doheadrequest(self, timeout = TIMEOUT):
        """
        Sends a HEAD request to the database node. The header returned by the database node contains some
        information on statistics. This information is stored in the headers object of the request instance.
        """

        self.headers = {}

        url = self.baseurl + self.querypath
        urlobj = urlsplit(url)
        
        conn = HTTPConnection(urlobj.netloc, timeout = timeout)
        conn.putrequest("HEAD", urlobj.path+"?"+urlobj.query)
        conn.endheaders()
        
        try:
            res = conn.getresponse()
        except socket.timeout as e:
            self.status = 408
            self.reason = "Socket timeout"
            raise TimeOutError

        self.status = res.status
        self.reason = res.reason

        if res.status == 200:
            headers = res.getheaders()
        elif res.status == 204:
            headers = [ ("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]
        elif res.status == 408:
            print("TIMEOUT")
            headers =  [("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]            
        else:
            print("STATUS: %d" % res.status)
            headers =  [("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]

        for key,value in headers:
            self.headers[key] = value
 
    def getlastmodified(self):
        """
        Returns the 'last-modified' date which has been specified in the
        Header of the requested document.
        """
        if not self.status == 200:
            self.doheadrequest()

        if 'last-modified' in self.headers:
            try:
                self.lastmodified = parse(self.headers['last-modified'])
            except Exception as e:
                print("Could not parse date %s" % self.headers['last-modified'])
                print(e)
        else:
            if self.status == 204:
                raise NoContentError('requets.getlastmodified')

            self.lastmodified = None

        return self.lastmodified

    def getspecies(self):
        """
        Requests all species of the database node and returns a result.Result instance which contains the inforation
        in the format specified by the model (specmodel.py).
        This is equal to sending a 'SELECT SPECIES' - query to the node.
        """

        querystring = "SELECT SPECIES WHERE ((InchiKey!='UGFAIRIUMAVXCW'))"
        self.setquery(querystring)
        result = self.dorequest()

        return result



