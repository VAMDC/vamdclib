# -*- coding: utf-8 -*-

from urllib import urlencode,quote
from nodes import *

QUERY_SPECIES="SELECT SPECIES"

DICT_RESTRICTIONS=[
    'Inchikey',
    'FrequencyFrom',
    'FrequencyTo',
    ]

class Query(object):

    #QUERY=SELECT+ALL+WHERE+((+MoleculeInchiKey%3D'UGFAIRIUMAVXCW-ZCWHFVSRSA-N'))"


    def __init__(self, Query = None, Request='doQuery', Lang='VSS2', Format='XSAMS'):

        self.Request=Request
        self.Lang = Lang
        self.Format =Format
        if Query is not None:
            self.set_query(Query)


    def set_node(self, node):
        self.Node = node
        if not hasattr(self.Node,'url') or len(self.Node.url)==0:
            print "Warning: Url of this node is empty!"
        else:
            self.Requesturl = self.get_sync_url(self.Node.url)
        

    def set_query(self, query):

        if type(query)==QueryBuilder:
            self.QueryBuilder=query
            self.Query = query.Query

        else:
            self.Query=query
            
        
    def get_sync_url(self, nodeurl):
        """
        Combines the query information and builds the query-url-string

        nodeurl = access-url of a single VAMDC -tap node

        Returns: queryurl (string) for the VAMDC-tap node
        """

        if not nodeurl or len(nodeurl)==0:
            # Raise exception or return nothing
            return ""

        if not self.Query or len(self.Query)==0:
            # Raise exception or return nothing
            return ""

        if nodeurl[-1]=='/':
            nodeurl+='sync?'
        else:
            nodeurl+='/sync?'

            
#        self.Requesturl = "%sREQUEST=%s&LANG=%s&FORMAT=%s&QUERY=%s" % (nodeurl, self.Request, self.Lang, self.Format, quote(self.Query))
        
        return "%sREQUEST=%s&LANG=%s&FORMAT=%s&QUERY=%s" % (nodeurl, self.Request, self.Lang, self.Format, quote(self.Query))
        

class QueryBuilder(object):

    def __init__(self, Requestables='ALL', Restrictions=None):

        if hasattr(Requestables,'__iter__'):
            self.Query='SELECT %s ' % ','.join(Requestables)
        else:
            self.Query='SELECT %s ' % Requestables
        
        if Restrictions.has_key('inchikey'):
            if hasattr(Restrictions['inchikey'],'__iter__') and len(Restrictions['inchikey'])>0:
                inchi='(InchiKey='+'\''+'\' AND InchiKey=\''.join(Restrictions['inchikey'])+'\')'
            elif len(Restrictions['inchikey'])>0:
                inchi="InchiKey='%s' " % Restrictions['inchikey']
            else:
                pass


        self.Query += " WHERE %s " % inchi
        
                
