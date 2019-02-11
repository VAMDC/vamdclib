# -*- coding: utf-8 -*-

import sys
import os
from copy import deepcopy

if sys.version_info[0] == 3:
    from .results import *
else:
    from results import *

NAMESPACE='http://vamdc.org/xml/xsams/0.3'
NSMAP = {'ns':NAMESPACE}

# Helper function to test if an object is a list or tuple
isiterable = lambda obj: hasattr(obj, '__iter__')

def match_states(states1, states2):
    """
    Identifies equal states
    """
    matches=[]
    for state1 in states1:
        for state2 in states2:
            #if states2[state2].QuantumNumbers == states1[state1].QuantumNumbers:
            if states2[state2] == states1[state1]:
                print(state1, state2)
                matches.append([state1,state2])

    return matches




def init_test():

    nl=Nodelist()
    cdms=nl.nodes[14]
    basecol=nl.nodes[0]

    qb=QueryBuilder(Restrictions={'inchikey':'UGFAIRIUMAVXCW-UHFFFAOYSA-N'})

    q_cdms=Query(qb)
    q_cdms.set_node(cdms)

    r_cdms=Result()
    r_cdms.set_query(q_cdms)
    r_cdms.do_query()
    r_cdms.populate_model()

    q_basecol=Query(qb)
    q_basecol.set_node(basecol)

    r_basecol=Result()
    r_basecol.set_query(q_basecol)
    r_basecol.do_query()
    r_basecol.populate_model()

    return r_cdms, r_basecol



def append_element(parent, child):
    """
    Appends a deepcopy of the element 'child' to the 'parent' element.
    """

    parent.append(deepcopy(child))
    

#for i in xml.xpath('//*[ns:StateRef="SBASET73-1"]', namespaces=NSMAP):
#    print i.tag, i.xpath('ns:StateRef', namespaces=NSMAP)[0].text 
#    r=i.xpath('ns:SpeciesRef',namespaces=NSMAP)   
#    print len(r), r[0].text

def append_coltranss(xml, coltrans):
    """
    Appends collisional transitions to an xsams.xml document.

    xml = xml document which is defined by the XSAMS-schema 
    coltrans = list of 'CollisionalTransition' elements
    """

    # Check if Processes - element exists:
    procs = xml.xpath('//ns:Processes', namespaces=NSMAP)
    if len(procs)==0:
        procs = etree.SubElement(xml, "{%s}Processes" % NSMAP['ns'])
        xml.append(procs)
    elif len(procs)>1:
        # Raise error
        print("There should be only one Processes element")
        return
    else:
        procs = procs[0]


    # Check if Collision Element exists
    collisions = procs.xpath('ns:Collisions', namespaces = NSMAP)
    if len(collisions)==0:
        collisions = etree.SubElement(xml, "{%s}Collisions" % NSMAP['ns'])
        procs.append(collisions)
    elif len(collisions)>1:
        # Raise error
        print("There should be only one Collisions element")
        return
    else:
        collisions=collisions[0]

    species_list=[]
    for col in coltrans:
        # todo: there should be a check if the collional transition already exists!
        
        append_element(collisions, col)

        # get related elements and attach them to the document
        
        # get source

        # get specie
        for i in col.xpath('.//ns:SpeciesRef', namespaces=NSMAP):
            if i.text not in species_list:
                species_list.append(i.text)
        # get function

        # get method


    #species = col.xpath('//[ns:Molecule',namespaces=NSMAP)

    return species_list #, species


def append_specie(xml, specie):

    # Check if specie is Molecule, Atom,
    
    # Check if Processes - element exists:
    species = xml.xpath('//ns:Species', namespaces=NSMAP)
    if len(species)==0:
        species = etree.SubElement(xml, "{%s}Species" % NSMAP['ns'])
        xml.append(species)
    elif len(species)>1:
        # Raise error
        print("There should be only one Species element")
        return
    else:
        species = species[0]

    if specie.tag == '{%s}Molecule' % NSMAP['ns']:

        # Check if Processes - element exists:
        mols = xml.xpath('//ns:Molecules', namespaces=NSMAP)
        if len(mols)==0:
            mols = etree.SubElement(xml, "{%s}Molecules" % NSMAP['ns'])
            xml.append(mols)
        elif len(mols)>1:
            # Raise error
            print("There should be only one Molecules element")
            return
        else:
            mols = mols[0]

        append_element(mols, specie)

    elif specie.tag == '{%s}Ion' % NSMAP['ns']:

        atoms = xml.xpath('//ns:Atoms', namespaces=NSMAP)
        if len(atoms)==0:
            atoms = etree.SubElement(xml, "{%s}Atoms" % NSMAP['ns'])
            xml.append(atoms)
        elif len(atoms)>1:
            # Raise error
            print("There should be only one Molecules element")
            return
        else:
            atoms = atoms[0]
        
        
def get_or_create_mainelement(xml, tag):

        el = xml.xpath('//ns:%s' % tag, namespaces=NSMAP)
        if len(el)==0:
            el = etree.SubElement(xml, "{%s}%s" % (NSMAP['ns'],tag))
            xml.append(el)
        elif len(el)>1:
            # Raise error
            print("There should be only one element")
            return
        else:
            el = el[0]

        return el

    
    
def get_species_element(xml,id):

    try:
        el = xml.xpath('//*[@speciesID="%s"]' %id ,namespaces=NSMAP)
    except Exception as e:
        print("Could not get specie: %s" % e)
        return None


    return el[0]



def apply_stylesheet(xml, xsl):
    
    xsl=e.XSLT(e.parse(xsl))
    return xsl(xml)
