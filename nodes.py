# -*- coding: utf-8 -*-
"""
This module defines classes and methods to manage data associated with VAMDC nodes. It provides
functionality to retrieve a list of registered VAMDC nodes and to handle data such as urls of these
nodes.
"""
import sys
import os

if sys.version_info[0] == 3:
    try:
        from .registry import *
    except:
        print("Suds package not available. Load Vamdc-Nodes from static file")
        from .local_registry import *
    from . import query as q
    from . import request as r
else:
    try:
        from registry import *
    except:
        print("Suds package not available. Load Vamdc-Nodes from static file")
        from local_registry import *
    import query as q
    import request as r


class Nodelist(object):
    """
    This class provides a list of database nodes and methods
    which are related to a list of nodes.
    """
    def __init__(self):
        """
        An instance of Nodelist contains a list of registered VAMDC nodes. This list is retrieved
        via querying the VAMDC registry by default during initialization of the instance.
        """
        self.nodes = []
        for node in getNodeList():
            self.nodes.append(Node(node['name'], url=node['url'], referenceUrl=node['referenceUrl'],identifier = node['identifier'], maintainer=node['maintainer'], returnables=node['returnables']))

    def __repr__(self):
        """
        Returns a string which contains a list of all VAMDC node names
        """
        returnstring = ""
        for node in self.nodes:
            returnstring += "%s\n" % node.name

        return returnstring

    def getnode(self, identifier):
        """
        Return a nodes.Node instance for the given ivo-identifier. 
        """
        for node in self.nodes:
            if node.identifier == identifier:
                return node
        return None
   
    def findnode(self, searchstring):
        """
        This method tries to identify a VAMDC node by the specified 'searchstring'. It will return
        a instance of nodes.Node if the node could be uniquely identified. Otherwise it will print out all
        nodes which match the searchstring.

        :param str searchstring: The string which looked for in the nodes name and ivo-identifier

        :return: The node or a list of nodes which matches the searchstring.
        :rtype: nodes.Node
        """
        nodes_match = []
        for node in self.nodes:
            if searchstring in node.identifier or searchstring in node.name:
                nodes_match.append(node)
        if len(nodes_match) == 1:
            return nodes_match[0]
        else:
            return nodes_match

    def __iter__(self):
        return self.nodes.__iter__()
        

class Node(object):
    """
    This class contains informations and methods associated with one (VAMDC) database node,
    such as its access url (for database queries) and its name.    

    :ivar name: Name of the VAMDC node
    :ivar url: Url of the VAMDC node 
    :ivar identifier: IVO-Identifier of the Node
    """
    def __init__(self, name, url=None, referenceUrl=None, identifier=None , maintainer=None, returnables=None):
        self.name = name
        self.url = url
        self.referenceUrl = referenceUrl
        self.identifier = identifier
        self.maintainer = maintainer
        self.returnables = returnables

    def __repr__(self):
        """
        Returns the node's name.
        """
        
        return self.name
        
    
    def get_species(self):
        """
        Queries all species from the database-node via TAP-XSAMS request and
        Query 'Select Species'. The list of species is saved in object species.
        Note: This does not work for all species !
        """
        # Some nodes do not understand this query at all
        # others do not understand the query SELECT SPECIES
        # therefore the following query is a small workaround for some nodes
        query=q.Query("SELECT SPECIES WHERE ((InchiKey!='UGFAIRIUMAVXCW'))")                

        req = r.Request()
        req.setnode(self)
        req.setquery(query)
        result = req.dorequest()
        
        try:
            self.Molecules = result.data['Molecules']
        except:
            pass
        try:
            self.Atoms = result.data['Atoms']
        except:
            pass

    def print_species(self):
        """
        prints out the list of species to stdout if they can be accessed with a SELECT SPECIES - Query
        """

        if not (hasattr(self, 'Atoms') or hasattr(self, 'Molecules')):
                self.get_species()
                
        try:
            print("List of Atoms: ")
            for atom in self.Atoms:
                print("%s" % self.Atoms[atom])
    
            print("List of Molecules: ")
            for molecule in self.Molecules:
                print("%s" % self.Molecules[molecule])

        except Exception as e:
            print("Could not retrieve list of species: %s" % e)
            
