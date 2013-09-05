# -*- coding: utf-8 -*-
try:
    from lxml import objectify
    is_available_xml_objectify = True
except ImportError:
    is_available_xml_objectify = False
 
from xml.etree import ElementTree
import urllib2
from specmodel import *
import query as q

from urlparse import urlparse
from httplib import HTTPConnection

from dateutil.parser import parse

XSD = "http://vamdc.org/xml/xsams/1.0"

class Result(object):

    def __init__(self, xml=None, source=None):

        self.Source = source
        self.Xml = xml
        
        #if self.Xml is None:
        #    self.get_xml(self.Source)

    def set_query(self,query):
        if type(query)==q.Query:
            self.Source = query
        else:
            print "Warning: this is not a query object"

    def do_query(self):
        self.get_xml(self.Source.Requesturl)


    def doHeadRequest(self, timeout = 20):
        """
        Does a HEAD request on the given url.
        A list of 'vamdc' - statistic objects is returned
        """
    
        urlobj = urlparse(self.Source.Requesturl)

        try:
            conn = HTTPConnection(urlobj.netloc, timeout = timeout)
            conn.request("HEAD", urlobj.path+"?"+urlobj.query)
            res = conn.getresponse()
        except:
            # error handling has to be included
            vamdccounts = [] #[('error', 'no response')]
            return vamdccounts        

        return_dict = {}

        for item in res.getheaders():
            return_dict[item[0]] = item[1]
#        if res.status == 200:
#            vamdccounts = [item for item in res.getheaders() if item[0][0:5]=='vamdc']
#            content = [item for item in res.getheaders() if item[0][0:7]=='content']
#        elif res.status == 204:
#            vamdccounts = [ ("vamdc-count-species",0),
#                            ("vamdc-count-states",0),
#                            ("vamdc-truncated",0),
#                            ("vamdc-count-molecules",0),
#                            ("vamdc-count-sources",0),
#                            ("vamdc-approx-size",0),
#                            ("vamdc-count-radiative",0),
#                            ("vamdc-count-atoms",0)]
#        else:
#            vamdccounts =  [("vamdc-count-species",0),
#                            ("vamdc-count-states",0),
#                            ("vamdc-truncated",0),
#                            ("vamdc-count-molecules",0),
#                            ("vamdc-count-sources",0),
#                            ("vamdc-approx-size",0),
#                            ("vamdc-count-radiative",0),
#                            ("vamdc-count-atoms",0)]
            
        return return_dict



    def getChangeDate(self):
        rdict = self.doHeadRequest()
        try:
            d = parse(rdict['last-modified'])
        except Exception, e:
            print rdict
            print e
        
        return d

        
    def get_xml(self, source):

        try:
            xml = urllib2.urlopen(source)
            xml = xml.read()
        except urllib2.HTTPError,e:
            print "Could not retrieve data from url %s: %s" % (source, e)
        except ValueError:
            xml = etree.parse(source)


        try:
            if not isinstance(xml, str):
                xml = etree.tostring(xml)
        except Exception, e:
            print "parser error (to string): %s " % e

        self.Xml=xml

    def objectify(self):
        """
        Takes a xml source an returns it as an object
    
        The source can be any of the following:
    
        - a file name/path
        - a file object
        - a file-like object
        - a URL using the HTTP or FTP protocol
        """

        if not is_available_xml_objectify:
            print "Module lxml.objectify not available"
            return
        
        try:
            self.root = objectify.XML(self.Xml)
        except ValueError:
            self.Xml=etree.tostring(self.Xml)
            self.root = objectify.XML(self.Xml)
        except Exception, e:
            print "Objectify error: %s " % e

    
    def populate_model(self):
        """
        Populates classes of specmodel
        """

        if not hasattr(self, 'root'):
            self.root = ElementTree.fromstring(self.Xml)
        #    self.objectify()

        self.data = populate_models(self.root, add_states=True)


    def get_vibstates(self):

        vibs = {}
        for qn in self.States:
            vib = ''
            for l in self.States[qn].QuantumNumbers.qns:
                if isVibrationalStateLabel(l):
                    vib += "%s=%s, " % (l,self.States[qn].QuantumNumbers.qns[l])
            # remove last ', ' from the string
            vib = vib[:-2]
            try:
                if vib not in vibs[self.States[qn].SpecieID]:
                    vibs[self.States[qn].SpecieID].append(vib)
            except KeyError:
                vibs[self.States[qn].SpecieID] = [vib]
                    
        return vibs

    def get_process_class(self):

        classes = {}
        for trans in self.root.Processes.Radiative.RadiativeTransition:
            codes = []
            for code in trans.ProcessClass.Code:
                codes.append(code)
            try:
                if codes not in classes[str(trans.SpeciesRef)]:
                    classes[str(trans.SpeciesRef)].append(codes)
            except KeyError:
                classes[str(trans.SpeciesRef)] = [codes]

        return classes
    
    def validate(self):

        if not hasattr(self, 'xsd'):
            self.xsd=etree.XMLSchema(etree.parse(XSD))
        xml = etree.fromstring(self.Xml)

        return self.xsd.validate(xml)


    def apply_stylesheet(xslt):
        """
        Applys a stylesheet to the xml object and returns
        the result as string.

        xslt = url / file which contains the stylesheet

        returns:

        String (the result of the operation)
        """
        # To be implemented
        pass


