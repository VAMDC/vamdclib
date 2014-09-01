# -*- coding: utf-8 -*-
try:
    from lxml import objectify
    is_available_xml_objectify = True
except ImportError:
    is_available_xml_objectify = False
 
from xml.etree import ElementTree
import urllib2

from settings import *
import query as q
import results as r
import nodes

from urlparse import urlparse
from httplib import HTTPConnection, urlsplit, HTTPException, socket

from dateutil.parser import parse

XSD = "http://vamdc.org/xml/xsams/1.0"

class TimeOutError(HTTPException):
    def __init__(self):
        HTTPException.__init__(self, 408, "Timeout")
        self.strerror = "Timeout"
        
        
class Request(object):

    def __init__(self, node = None, query = None):

        self.status = 0
        self.reason = "INIT"

        if node != None:
            self.setnode(node)
            
        if query != None:
            self.setquery(query)

    def setnode(self, node):
        self.status = 0
        self.reason = "INIT"

        if type(node) == nodes.Node:
            self.node = node
            
            if not hasattr(self.node,'url') or len(self.node.url)==0:
#                print "Warning: Url of this node is empty!"
                pass
            else:
                self.baseurl = self.node.url
                if self.baseurl[-1]=='/':
                    self.baseurl+='sync?'
                else:
                    self.baseurl+='/sync?'

    def setbaseurl(self, baseurl):
        self.baseurl = baseurl
        if self.baseurl[-1]=='/':
            self.baseurl+='sync?'
        else:
            self.baseurl+='/sync?'

    def setquery(self,query):
        self.status = 0
        self.reason = "INIT"
        
        if type(query)==q.Query:
            self.query = query
            self.setquerypath()
        elif type(query) == str or type(query) == unicode:
            self.query = q.Query(Query = query)
            self.setquerypath()
        else:
#            print type(query)
#            print "Warning: this is not a query object"
            pass
        

    def setquerypath(self):
        """
        Sets the querypath which is appended to the nodes 'base'-url.
        """
        self.querypath = "REQUEST=%s&LANG=%s&FORMAT=%s&QUERY=%s" % ( self.query.Request,
                                                                     self.query.Lang,
                                                                     self.query.Format,
                                                                     urllib2.quote(self.query.Query))
        

    def dorequest(self, timeout = TIMEOUT, HttpMethod = "POST", parsexsams = True):

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
        Does a HEAD request on the given url.
        A list of 'vamdc' - statistic objects is returned
        """

        self.headers = {}

        url = self.baseurl + self.querypath
        urlobj = urlsplit(url)
        
        conn = HTTPConnection(urlobj.netloc, timeout = timeout)
        conn.putrequest("HEAD", urlobj.path+"?"+urlobj.query)
        conn.endheaders()
        
        try:
            res = conn.getresponse()
        except socket.timeout, e:
            self.status = 408
            self.reason = "Socket timeout"
            raise TimeOutError

        self.status = res.status
        self.reason = res.reason

        if res.status == 200:
            for key,value in res.getheaders():
                self.headers[key] = value
        elif res.status == 204:
            self.headers = [ ("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]
        elif res.status == 408:
            print "TIMEOUT"
            self.headers =  [("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]            
        else:
            print "STATUS: %d" % res.status
            self.headers =  [("vamdc-count-species",0),
                            ("vamdc-count-states",0),
                            ("vamdc-truncated",0),
                            ("vamdc-count-molecules",0),
                            ("vamdc-count-sources",0),
                            ("vamdc-approx-size",0),
                            ("vamdc-count-radiative",0),
                            ("vamdc-count-atoms",0)]

    def getlastmodified(self):

        if not self.status == 200:
            self.doheadrequest()

        if self.headers.has_key('last-modified'):
            try:
                self.lastmodified = parse(self.headers['last-modified'])
            except Exception, e:
                print "Could not parse date %s" % self.headers['last-modified']
                print e
        else:
            self.lastmodified = None

        return self.lastmodified

    def getspecies(self):
        """
        Queries species of the node and returns the result with already
        populated data model.
        """

        querystring = "SELECT SPECIES WHERE ((InchiKey!='UGFAIRIUMAVXCW'))"
        self.setquery(querystring)
        result = self.dorequest()
        #result.populate_model()

        return result



