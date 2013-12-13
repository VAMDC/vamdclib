# -*- coding: utf-8 -*-
import functions 
import numpy
import sys

NAMESPACE='http://vamdc.org/xml/xsams/1.0'

# some usefull functions
def split_datalist(datalist):
    """
    """
    return datalist.text.split(" ")

def get_value(element):
    """
    Just returns the value of an element
    """
    return element.text

def get_attributes(element):
    """
    Returns a list of attributes-tuples (attribute, value) 
    """
    return element.items()

def convert_tabulateddata(item):
    """
    Converts an element of type {..xsams..}TabulatedData into a dictionary
    with elements from X as key and elements from Y as values

    Returns:

    datadict = (dictionary) with datapoints
    xunits = (string) unit of key elements
    yunits = (string) containing unit of value elements
    comment = (string)
    """
    
    x = item.find("{%s}X/{%s}DataList" % (NAMESPACE, NAMESPACE) ).text.split(" ")
    y = item.find("{%s}Y/{%s}DataList" % (NAMESPACE, NAMESPACE) ).text.split(" ")
    xunits = item.find("{%s}X" % (NAMESPACE) ).get('units')
    yunits = item.find("{%s}Y" % (NAMESPACE) ).get('units')
    comment = item.find("{%s}Comments" % (NAMESPACE)).text
    
    datadict = {}
    for i in range(len(x)):
        datadict[x[i]]=y[i]

    return {'data':datadict, 'xunits:':xunits, 'yunits':yunits, 'comment':comment}

def remove_namespace(tag):
    """
    Returns tag without namespace
    """
    return tag[tag.find('}')+1:]

def construct_model(dictionary):
    """
    This method constructs the MODEL-Dictionaries. A Dictionary which contains
    the key/value - pairs (fieldname, path_to_value) will be translated into
    executable code (evaluated with eval() ). The model-dictionary which is
    evaluated and returned depends on the xml-parser/library which is used.
    If the library is changed (e.g. to lxml). This function has to be replaced
    or changed.

    Syntax of the input-dictionary:
    fieldname:path (tags without namespace connected with dot. Multiple occurances
              are indicated by '[]' and functions which have to be applied are
              appended at the end of the string with preceeding '\\'.

              
    """
    model = {}
    for field in dictionary:
        code = ""
        code_add = ""
        iterator_code = None
        
        if dictionary[field].find("\\")>-1:
            path_array, function = dictionary[field].split("\\")
            path_array = path_array.split(".")
        else:
            function = None
            path_array = dictionary[field].split(".")
            
        for tag in path_array:
            # is an attribute

            if len(tag) == 0:
                pass
            elif tag[0] == '@':
                code_add = "get('%s')" % (tag[1:],)
                # attribute can only at the last position
                break
            # xpath expression -> do not attach namespace
            elif tag[-2:] == '[]' and tag[0] in ['*','.','/']:
                iterator_code = "self.xml.findall('%s%s')" % (code, tag[:-2])
                code = ""
            elif tag[-2:] == '[]':
                iterator_code = "self.xml.findall('%s{%s}%s')" % (code, NAMESPACE, tag[:-2])
                code = ""
            elif tag[0] in ['*','.','/']:
                code += "%s/" % tag
            # regular element -> attach namespace
            else:
                code += "{%s}%s/" % (NAMESPACE, tag)
                # put path into find() if it is the last tag

        # create code to generate a list if there was an iterable element
        if iterator_code is not None:
            if len(code) == 0:
                if function is not None:
                    if function == 'self':
                        code = "[el for el in %s]" % (iterator_code)
                    else:    
                        code = "[%s(el) for el in %s]" % (function, iterator_code)
                elif len(code_add) == 0:
                    code = "[el.text for el in %s]" % (iterator_code)
                else:
                    code = "[el.%s for el in %s]" % (code_add, iterator_code)
            else:
                if function is not None:
                    if function == 'self':
                        code = "[el.find('%s') for el in %s]" % (code[:-1], iterator_code)
                    else:
                        code = "[%s(el.find('%s')) for el in %s]" % (function, code[:-1], iterator_code)
                elif len(code_add) == 0:
                    code = "[el.find('%s').text for el in %s]" % (code, iterator_code)
                else:
                    code = "[el.find('%s').%s for el in %s]" % (code, code_add, iterator_code)
                
                    
        else:
            if len(code) == 0:
                if function is not None:
                    if function == 'self':
                        code = "self.xml"
                    else:
                        code = "%s(self.xml)" % (function,)
                elif len(code_add) > 0:
                    code = "self.xml.%s" % (code_add,)
                else:
                    print "ERROR --------" 
            else:
                if function is not None:
                    if function == 'self':
                        code = "self.xml.find('%s')" % (code[:-1],)
                    else:
                        code = "%s(self.xml.find('%s'))" % (function, code[:-1],)
                elif len(code_add) > 0:
                    code = "self.xml.find('%s').%s" % (code[:-1], code_add,)
                else:
                    code = "self.xml.find('%s').text" % (code[:-1],)
        model[field] = code
    return model

class Model(object):
    """
    Defines the general Model-Class from which all Model-classes are
    inherited. 
    """
    def __init__(self, xml):
        self.xml = xml
        
        if self.xml is not None:
            self.readXML(self.xml)
    
    def additem(self, item, value):
        """
        Adds a new element to the model. If the element name
        contains a colon then a dictionary based on the value
        preding the colon is created and the value is stored
        in this dictionary
        """
        if item.find(":") == -1:
            try:
                setattr(self, item, value)
            except:
                pass
        else:
            item_dict, item = item.split(":")
            if not self.__dict__.has_key(item_dict):
                setattr(self, item_dict, {})
            self.__dict__[item_dict][item] = value

    def readXML(self, xml):
        for item in self.DICT:
            try:
                value = eval("%s" % self.DICT[item])
                self.additem(item, value )
            except AttributeError:
                #print "Could not evaluate %s" % el
                pass

            # check for attributes
##            try:
##                for attribute in item.keys():
##                    self.additem(el+attribute.capitalize(), item.get(attribute))
##            except:
##                pass

                
def _construct_dictmodelclass(model_definitions, module):
    """
    Creates and returns a Dictionary Class (e.g. for Molecules).
    The elements of the dictionary are usually Model-Classes
    (e.g. class Molecule), which are defined by _construct_class
    """
    class _DictModel(dict):
        DICT = construct_model(model_definitions['Dictionary'])
        def __init__(self, xml):
            dict.__init__(self)
            self.xml = xml
            for item in eval("%s" % self.DICT[model_definitions['Name']]):
                element = module.__dict__[model_definitions['Type']](item)
                self[element.Id] = element
                             
    return _DictModel
        
def _construct_class(model_definitions, module = None):
    """
    Creates and returns a Model-Class (e.g. for a Molecule)
    """
    class _Model(Model):
        DICT = construct_model(model_definitions['Dictionary'])
           
        def __repr__(self):
            retval = ""
            for field in model_definitions['representation_fields']:
                try:
                    retval += "%s " % self.__dict__[field]
                except KeyError:
                    retval += "None "
            return retval
        
    if model_definitions.has_key('methods'):
        for method in model_definitions['methods']:
            setattr(_Model, method['name'], method['method'])

    return _Model

def register_models(DICT_MODELS, module):
    """
    Creates classes and add them to this packages as well as
    the package which calls this method

    DICT_MODELS: Dictionary which defines Classes and its properties
    """
    for model in DICT_MODELS['model_types']:
        print "Register Class %s in %s" % (model['Name'], module.__name__)
        model_class = _construct_class(model)
        setattr(sys.modules[__name__], model['Name'], model_class )
        setattr(module, model['Name'], model_class )


    for model in DICT_MODELS['dict_types']:
        print "Register DictClass %s in %s" % (model['Name'], module.__name__)
        setattr(module, model['Name'], _construct_dictmodelclass(model, module))
        

