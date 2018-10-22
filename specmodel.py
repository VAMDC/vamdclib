# -*- coding: utf-8 -*-
import functions 
import numpy
import sys

from basemodel import *
#import basemodel

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

########################################################################
# Dictionaries for the Model-Layout
#
# These dictionaries contain the information which Classes are generated
# and which fields they have. The key / value pair is the fieldname and
# a path to the element in the XSAMS (XML) - Tree. Each child is connected
# to its parent by ".". Brackets "[]" indicate that there are multiple
# elements of the same type which have to be looped over. A function
# can be applied to an element. The function name has to be connected to
# the path by "\\".
#-------------------------------------------------------------------------

RADIATIVETRANS_DICT = {
    "Id":"@id",
    "LowerStateRef":"LowerStateRef",
    "UpperStateRef":"UpperStateRef",
    "FrequencyValue":"EnergyWavelength.Frequency.Value",
    "FrequencyAccuracy":"EnergyWavelength.Frequency.Accuracy",
    "TransitionProbabilityA":"Probability.TransitionProbabilityA.Value",
    "IdealisedIntensity":"Probability.IdealisedIntensity.Value",
    "Multipole":"Probability.Multipole",
    "SpeciesID":"SpeciesRef",
    "ProcessClass":"ProcessClass.Code[]",
    }

STATES_DICT = {
    "Id":"@stateID",
    "StateID":"@stateID",
#    "SpecieID":"getparent().get('speciesID')",
#    "InChIKey":"getparent().MolecularChemicalSpecies.InChIKey",    
    "StateEnergyValue":"MolecularStateCharacterisation.StateEnergy.Value",
    "StateEnergyUnit":"MolecularStateCharacterisation.StateEnergy.Value.@units",
    "StateEnergyOrigin":"MolecularStateCharacterisation.StateEnergy.@energyOrigin",
    "TotalStatisticalWeight":"MolecularStateCharacterisation.TotalStatisticalWeight",
    "NuclearSpinIsomerName":"MolecularStateCharacterisation.NuclearSpinIsomer.Name",
    "NuclearSpinIsomerLowestEnergy":"MolecularStateCharacterisation.NuclearSpinIsomer.@lowestEnergyStateRef",
    "QuantumNumbers":"Case\\QuantumNumbers",
    }

ATOMIC_STATES_DICT = {
    "Id":"@stateID",
    "StateID":"@stateID",
    "StateEnergyValue":"AtomicNumericalData.StateEnergy.Value",
    "StateEnergyUnit":"AtomicNumericalData.StateEnergy.Value.@units",
    "TotalStatisticalWeight":"AtomicNumericalData.StatisticalWeight",
#    "QuantumNumbers:J":"AtomicQuantumNumbers.TotalAngularMomentum",
#    "QuantumNumbers:F":"AtomicQuantumNumbers.HyperfineMomentum",
#    "QuantumNumbers:L":"AtomicComposition.Component.Term.LS.L.Value",
#    "QuantumNumbers:S":"AtomicComposition.Component.Term.LS.S",
#    "QuantumNumbers":"Case\\QuantumNumbers",
    "QuantumNumbers":"\\AtomQN",
    }

ATOMQN_DICT = {
    "Id":"@stateID",
    "qn_dict:J":"AtomicQuantumNumbers.TotalAngularMomentum",
    "qn_dict:F":"AtomicQuantumNumbers.HyperfineMomentum",
    "qn_dict:L":"AtomicComposition.Component.Term.LS.L.Value",
    "qn_dict:S":"AtomicComposition.Component.Term.LS.S",
}

ATOMS_DICT = {
    "Id":"Isotope.Ion.@speciesID",
    "SpeciesID":"Isotope.Ion.@speciesID",
    "VAMDCSpeciesID":"Isotope.Ion.InChIKey",
    "ChemicalElementNuclearCharge":"ChemicalElement.NuclearCharge",
    "ChemicalElementSymbol":"ChemicalElement.ElementSymbol",
    "MassNumber":"Isotope.IsotopeParameters.MassNumber",
    "Mass":"Isotope.IsotopeParameters.Mass.Value",
    "MassUnit":"Isotope.IsotopeParameters.Mass.Value.@units",
    "IonCharge":"Isotope.Ion.IonCharge",
    "InChIKey":"Isotope.Ion.InChIKey",
    "InChI":"Isotope.Ion.InChI",
    "Comment":"Isotope.Comments",
    "States":"Isotope.Ion.AtomicState[]\\AtomState",
    }

MOLECULES_DICT = {
    "Id":"@speciesID",
    "SpeciesID":"@speciesID",
    "ChemicalName":"MolecularChemicalSpecies.ChemicalName.Value",
    "Comment":"MolecularChemicalSpecies.Comment",
    "InChI":"MolecularChemicalSpecies.InChI",
    "InChIKey":"MolecularChemicalSpecies.InChIKey",
    "VAMDCSpeciesID":"MolecularChemicalSpecies.VAMDCSpeciesID",
#    "ChemicalName":"findtext('{"+NAMESPACE+"}MolecularChemicalSpecies/{"+NAMESPACE+"}MoleculeStructure')",
    "OrdinaryStructuralFormula":"MolecularChemicalSpecies.OrdinaryStructuralFormula.Value",
    "MolecularWeight":"MolecularChemicalSpecies.StableMolecularProperties.MolecularWeight.Value",
    "StoichiometricFormula":"MolecularChemicalSpecies.StoichiometricFormula",
    "PartitionFunction":"MolecularChemicalSpecies.PartitionFunction[]\\Partitionfunctions",
    "States":"MolecularState[]\\State",
    }

PARTITIONFUNCTIONS_DICT = {
#    "SpeciesID":"getparent().getparent().get('speciesID')",
    "NuclearSpinIsomer":"NuclearSpinIsomer.Name",    
    "PartitionFunctionT":"T.DataList\\split_datalist",    
    "PartitionFunctionQ":"Q.DataList\\split_datalist",    
    "Units":"T.@units",
    "Comments":"Comments",
    }

COLLISIONALTRANS_DICT = {
    "Id":"@id",
    "ProcessClassCode":"ProcessClass.Code",
    "Reactant":"Reactant[].SpeciesRef",
    "Product":"Product[].SpeciesRef",
    "DataDescription":"DataSets.DataSet.@dataDescription",
    "TabulatedData":"DataSets.DataSet.TabulatedData\\convert_tabulateddata",
    "X":"DataSets.DataSet.TabulatedData.X.DataList\\split_datalist",
    "XUnits":"DataSets.DataSet.TabulatedData.X.@units",
    "Y":"DataSets.DataSet.TabulatedData.Y.DataList\\split_datalist",
    "YUnits":"DataSets.DataSet.TabulatedData.Y.@units",
    "FitParameters":"DataSets.DataSet.FitData.FitParameters\\FitParameters",
    "FitMethod":"DataSets.DataSet.FitData.@methodRef",
    "FitComments":"DataSets.DataSet.FitData.FitComments",
    "FitSources":"DataSets.DataSet.FitData.SourceRef[]\\get_value",
    "Comment":"Comments",
    }

SOURCES_DICT = {
    "Id":"@sourceID",
    "AuthorList":"Authors.Author[].Name\\get_value",
    "Title":"Title",
    "Category":"Category",
    "Year":"Year",
    "SourceName":"SourceName",
    "Volume":"Volume",
    "PageBegin":"PageBegin",
    "PageEnd":"PageEnd",
    "DOI":"DigitalObjectIdentifier",
    }

QUANTUMNUMBERS_DICT = {
    "Case":"@caseID",
    "__qnelements__":"*.*[]\\self",
}

FITPARAMETERS_DICT = {
    "Function":"@functionRef",
    "Parameters":"FitParameter[]\\Parameter",
    "Arguments":"FitArgument[]\\Argument",
    }

FITPARAMETER_DICT = {
    "Name":"@name",
    "Units":"Value.@units",
    "Method":"@methodRef",
    "Value":"Value",
    "Accuracy":"Accuracy",
    "Comments":"Comments",
    "Source":"SourceRef",
}
FITARGUMENT_DICT = {
    "Name":"@name",
    "Units":"@units",
    "Description":"Description",
    "LowerLimit":"LowerLimit",
    "UpperLimit":"UpperLimit",
    }


#########################################################################
# Functions for the models
#
# If additional methods have to be added to a (Model) class they have to be
# defined here.
#------------------------------------
def states__eq__(self, other):
    """
    Compare if a states equals another one. This method will be
    connected to the States-Class and is needed to compare two states
    """
    
    # There should be also a check for specie's inchikey
    if self.InChIKey != other.InChIKey:
        return False
    # Check if quantum numbers agree
    if self.QuantumNumbers != other.QuantumNumbers:
        return False
    
    return True

def states__ne__(self, other):
    """
    Compare if a states does not equal another one. This method will be
    connected to the States-Class and is needed to compare two states
    """
    # There should be also a check for specie's inchikey
    if self.InChIKey != other.InChIKey:
        return True

    # Check if quantum numbers agree
    if self.QuantumNumbers != other.QuantumNumbers:
        return True

    return False

def partitionfunction_init(self, xml):
    """
    Creates a dictionary of Partitionfunctions (PF / Temperature) pairs
    """
    Model.__init__(self, xml)
    self.values = {}
    for i in range(len(self.PartitionFunctionT)):
        self.values[self.PartitionFunctionT[i]]=self.PartitionFunctionQ[i]

def collisionaltrans_init(self, xml):
    """
    """
    Model.__init__(self, xml)
    self.data = {}
    try:
        for i in range(len(self.X)):
            self.data[self.X[i]]=self.Y[i]
    except AttributeError:
        pass

def source_init(self, xml):
    Model.__init__(self, xml)
    if 'AuthorList' in self.__dict__:
        self.Authors = ", ".join(self.__dict__['AuthorList'])

def parse_qn(self, qn_element):
    """
    This method reads tag and attributes of the quantum number element
    and creates a new label including info on mode, nuclearSpinRef:
    e.g. F_N or v15

    returns:
      label : label of quantum number
      value : value
      attributes: dictionary of attributes
    """
    label = remove_namespace(qn_element.tag)
    value = get_value(qn_element)

    # loop through all the attributes
    attributes={}
    for item in  get_attributes(qn_element):
        if len(item)==2:
            attributes[item[0]]=item[1]
            if item[0]=='mode':
                label = label.replace('i',item[1])
                label = label.replace('j',item[1])
            elif item[0]=='j':
                label = label.replace('j',item[1])
            elif item[0]=='i':
                label = label.replace('i',item[1])
            elif item[0]=='nuclearSpinRef':
                label="%s_%s" % (label, item[1])
        elif len(item)==1:
            attributes[item[0]]=None
        else:
            pass

    return label, value, attributes

def quantumnumbers__init__(self, xml):

    self.qn_string = ""
    self.vibstate = ""
    
    Model.__init__(self, xml)

    # replace list of quantum numbers by dictionary
    self.qn_dict = {}
    for qn in self.__qnelements__:
        label, value, attributes = self.parse_qn(qn)
        self.qn_dict[label]= value
        #self.qns[j.tag.replace(self.ns,"")] = j
        self.qn_string += "%s = %s; " % (str(label),str(value))

        if isVibrationalStateLabel(label) and int(value)!=0:
            self.vibstate += "%s=%s, " % (str(label),str(value))
        # remove last ', ' from the string
    if self.vibstate == '':
        self.vibstate = 'v=0'
    else:
        self.vibstate = self.vibstate[:-2]

def quantumnumbers__eq__(self,other):
    # Check if cases agree
    if self.Case != other.Case:
        return False
    # Check if the same quantum numbers are present in both descriptions
    #if self.qns.keys().sort() != other.qns.keys().sort():

    # check if quantum numbers agree;
    # Use 0, if vibrational state quantum numbers are not
    # explecitly defined, in one of the quantum number sets
    if len(self.qn_dict)< len(other.qn_dict):
        qns1=self.qn_dict
        qns2=other.qn_dict
    else:
        qns1=other.qn_dict
        qns2=self.qn_dict

    for qn in qns2:
        if qn in qns1:
            if qns1[qn]!=qns2[qn]:
                return False
        else:
            if qn not in ['v','vi'] or int(qns2[qn])!=0:
                return False
    return True

def quantumnumbers__ne__(self,other):
    return not self.__eq__(other)


def isVibrationalStateLabel(label):
    """
    Checks if the label defines a vibrational state
    """
    if label[0]!='v':
        return False
    try:
        int(label[1])
        return True
    except IndexError:
        return True
    except ValueError:
        return False

def atomqn__init__(self, xml):
    """
    """
    Model.__init__(self, xml)
    # Create a string represantative of the quantum numbers.
    self.qn_string = ""
    for qn in self.qn_dict:
        self.qn_string += "%s = %s; " % (str(qn),str(self.qn_dict[qn]))

#################################################################
# Dictionary to Control Generation of Model- and Dictionary -
# Classes
#----------------------------------------------------------------
DICT_MODELS = {
    'model_types':[
        {'Name':'FitParameters',
         'Dictionary':FITPARAMETERS_DICT,
         'representation_fields':('Function',),
         },
        {'Name':'Parameter',
         'Dictionary':FITPARAMETER_DICT,
         'representation_fields':('Name',),
         },
        {'Name':'Argument',
         'Dictionary':FITARGUMENT_DICT,
         'representation_fields':('Name',),
         },
        {'Name':'State',
         'Dictionary':STATES_DICT,
         'init_functions':None,
         'methods':[{'name':'__eq__',
                     'method':states__eq__},
                    {'name':'__ne__',
                     'method':states__ne__}
                    ],
         'representation_fields':('StateID', 'StateEnergyValue', 'StateEnergyUnit'),
         },
        {'Name':'AtomState',
         'Dictionary':ATOMIC_STATES_DICT,
         'init_functions':None,
         'representation_fields':('StateID', 'StateEnergyValue', 'StateEnergyUnit'),
         },        
        {'Name':'AtomQN',
         'Dictionary':ATOMQN_DICT,
         'init_functions':None,
         'methods':[{'name':'__init__',
                     'method':atomqn__init__},
                    ],
         },        
        {'Name':'QuantumNumbers',
         'Dictionary':QUANTUMNUMBERS_DICT,
         'init_functions':None,
#         'representation_fields':('SpeciesID', 'PartitionFunctionT'),
         'methods':[{'name':'__init__',
                     'method':quantumnumbers__init__},
                    {'name':'parse_qn',
                     'method':parse_qn},
                    {'name':'__eq__',
                     'method':quantumnumbers__eq__},
                    {'name':'__ne__',
                     'method':quantumnumbers__ne__},                    
                    ],
         },        
        {'Name':'Partitionfunctions',
         'Dictionary':PARTITIONFUNCTIONS_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'PartitionFunctionT'),
         'methods':[{'name':'__init__',
                     'method':partitionfunction_init},
                    ],
         },
        {'Name':'Atom',
         'Dictionary':ATOMS_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'ChemicalElementSymbol', 'ChemicalElementNuclearCharge', 'InChIKey'),
         },
        {'Name':'Molecule',
         'Dictionary':MOLECULES_DICT,
         'init_functions':None,
         'representation_fields':('SpeciesID', 'InChIKey', 'OrdinaryStructuralFormula', 'StoichiometricFormula', 'Comment'),
         },
        {'Name':'RadiativeTransition',
         'Dictionary':RADIATIVETRANS_DICT,
         'init_functions':None,
         'representation_fields':('Id', 'FrequencyValue', 'FrequencyAccuracy', 'TransitionProbabilityA'),
         },
        {'Name':'CollisionalTransition',
         'Dictionary':COLLISIONALTRANS_DICT,
         'init_functions':None,
         'representation_fields':('Id'),
         'methods':[{'name':'__init__',
                     'method':collisionaltrans_init},
                    ],
         },
        {'Name':'Source',
         'Dictionary':SOURCES_DICT,
         'init_functions':None,
         'representation_fields':('Id', 'Authors', 'SourceName', 'Volume', 'PageBegin', 'Year'),
         'methods':[{'name':'__init__',
                     'method':source_init},
                    ],
         },
        ],
    'dict_types':[
        {'Name':'Atoms',
         'Dictionary':{"Atoms":"Species.Atoms.Atom[]\\self"},
         'Type':'Atom'},
        {'Name':'Molecules',
         'Dictionary':{"Molecules":"Species.Molecules.Molecule[]\\self"},
         'Type':'Molecule'},
        {'Name':'RadiativeTransitions',
         'Dictionary':{"RadiativeTransitions":"Processes.Radiative.RadiativeTransition[]\\self"},
         'Type':'RadiativeTransition'},
        {'Name':'CollisionalTransitions',
         'Dictionary':{"CollisionalTransitions":"Processes.Collisions.CollisionalTransition[]\\self"},
         'Type':'CollisionalTransition'},
        {'Name':'Sources',
         'Dictionary':{"Sources":"Sources.Source[]\\self"},
         'Type':'Source'},
        ]
    }

register_models(DICT_MODELS, module = sys.modules[__name__] )

##################################################
# process xml-data
#-------------------------------------------------

def populate_models(xml, add_states=False):
    data = {}
    for item in DICT_MODELS['dict_types']:
        try:
            data[item['Name']] = eval("%s(xml)" % item['Name'])
        except Exception as e: # NameError:
            #print "Error: Could not evaluate %s" % item['Name']
            #print e
            pass
    if add_states and 'States' not in list(data.keys()):
        data['States'] = {}
        for SpeciesID in data['Molecules']:
            for state in data['Molecules'][SpeciesID].States:
                state.SpeciesID = SpeciesID
                data['States'][state.StateID] = state

        for SpeciesID in data['Atoms']:
            for state in data['Atoms'][SpeciesID].States:
                state.SpeciesID = SpeciesID
                data['States'][state.StateID] = state
            
    return data
    
    
def calculate_partitionfunction(states, temperature = 300.0):

    pfs = {}
    distinct_list = {}
    # create a distinct list of states
    for state in states:
        id = states[state].SpeciesID
        qn_string = states[state].QuantumNumbers.qn_string
        
        if not id in distinct_list:
            distinct_list[id] = {}
        distinct_list[id][qn_string] = states[state]

    for specie in distinct_list:
        pfs[specie] = 0
        for state in distinct_list[specie]:
            pfs[specie] += int(distinct_list[specie][state].TotalStatisticalWeight) * numpy.exp(-1.43878*float(distinct_list[specie][state].StateEnergyValue)/temperature)
            

    return pfs
        
