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

        if not hasattr(self, 'root') or self.root == None:
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


