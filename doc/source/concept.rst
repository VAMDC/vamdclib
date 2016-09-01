Concept of this library
=======================

The concept of this library is to provide methods to easily query, retrieve and to process atomic and molecular data
from VAMDC database nodes. The data will be provides as python dictionaries or lists. The layout of these dictionaries
is specified in specmodel.py in order to provide as much flexibility as possible and to simplify the adaptation to users needs. 
Python classes extending the type dictionary will be created during initialization. The layout in specmodel.py is separated
from the xml library used to parse and process the data. The xml - processing is located in basemodel.py and uses the 
simple ElementTree module from xml.etree, but can be replaced by other libraries such as lxml.etree by just replacing the
corresponding code in basemodel.py

Datamodel
---------

The layout of each class is defined in specmodel.py by python dictionaries. Keys in the dictionary will be translated into
field names of the class and the value specifies the path to the value in the xml-structure (similar to xpath definitions). Child elements are
connected by dots to their parent element. 

E.g.::

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

The path 'EnergyWavelength.Frequency.Value' will be translated by basemodel.py to the xpath 'EnergyWavelength/Frequency/Value'.
Functions which will be translated to xpath-functions can be attached to the path by "\\". 'ProcessClass.Code[]' indicates that a loop
over the element 'Code' has to be performed. Thus 'ProcessClass' will finally contain a list of codes. 

In addition, 'specmodel.py' contains a dictionary of all classes which shall be created. These are specified as 'model_types' 
in the dictionary DICT_MODELS. Functions which will be attached to the '__init__()' - Method of each class can be specified as
well as a list of field names which will be used to create a representational string.
Finally, The path to the location of the data in the XSAMS document has to be attached to the classes. This is done in 
'dict_types' in DICT_MODELS. 

E.g.::

  DICT_MODELS = {
      'model_types':[
          {'Name':'Molecule',
           'Dictionary':MOLECULES_DICT,
           'init_functions':None,
           'representation_fields':('SpeciesID', 
                                    'InChIKey', 
                                    'OrdinaryStructuralFormula', 
                                    'StoichiometricFormula', 
                                    'Comment'),
           },
          {'Name':'RadiativeTransition',
           'Dictionary':RADIATIVETRANS_DICT,
           'init_functions':None,
           'representation_fields':('Id', 
                                    'FrequencyValue', 
                                    'FrequencyAccuracy', 
                                    'TransitionProbabilityA'),
           },
           ... more types ...
          ],
      'dict_types':[
          {'Name':'Molecules',
           'Dictionary':{"Molecules":"Species.Molecules.Molecule[]\\self"},
           'Type':'Molecule'},
          {'Name':'RadiativeTransitions',
           'Dictionary':{"RadiativeTransitions":"Processes.Radiative.RadiativeTransition[]\\self"},
           'Type':'RadiativeTransition'},
          ]
      }

In this example the classes RadativeTransitions and Molecules will be created and populated with data from the XSAMS 
document at '/Species/Molecules/Molecule' and '/Processes/RadiativeTransitions', respectively.

