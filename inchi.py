# -*- coding: utf-8 -*-

import re

# dictionary with mass references used in the inchi-isotopic layer
atom_mass_reference = {
    "H":1, "He":4, "Li":7, "Be":9, "B":11, "C":12, "N":14, "O":16, "F":19, "Ne":20, "Na":23, "Mg":24, "Al":27, "Si":28,
    "P":31, "S":32, "Cl":35, "Ar":40, "K":39, "Ca":40, "Sc":45, "Ti":48, "V":51, "Cr":52, "Mn":55, "Fe":56, "Co":59,
    "Ni":59, "Cu":64, "Zn":65, "Ga":70, "Ge":73, "As":75, "Se":79, "Br":80, "Kr":84, "Rb":85, "Sr":88, "Y":89, "Zr":91,
    "Nb":93, "Mo":96, "Ru":101, "Rh":103, "Pd":106, "Ag":108, "Cd":112, "In":115, "Sn":119, "Sb":122, "Te":128, "I":127,
    "Xe":131, "Cs":133, "Ba":137, "La":139, "Ce":140, "Pr":141, "Nd":144, "Sm":150, "Eu":152, "Gd":157, "Tb":159, "Dy":163,
    "Ho":165, "Er":167, "Tm":169, "Yb":173, "Lu":175, "Hf":178, "Ta":181, "W":184, "Re":186, "Os":190, "Ir":192, "Pt":195,
    "Au":197, "Hg":201, "Tl":204, "Pb":207, "Bi":209, "Th":232, "U":238, } 
    
class InChI:
    """
    This class creates an InChI instance.
    It parses the information for an InChI and generates some useful informations out of the InChI,
    such as the stoichiometric formula, the massnumber, total charge

    inchi = InChI (The IUPAC International Chemical Identifier)
            example: inchi_example = '1S/CHN/c1-2/h1H/i2+1' which is the inchi of HC(15N)
    """
    
    dict_layers = {'c':'connections',
                   'h':'H_atoms',
                   'q':'charge',
                   'p':'protons',
                   'b':'stereo_dbond',
                   't':'stereo_sp3',
                   'm':'stereo_sp3_inverted',
                   's':'stereo_type',
                   'r':'reconnectMetals',
                   'rc':'reconnect_connections',
                   'rh':'reconnect_H_atoms',
                   'rq':'reconnect_charge',
                   'rp':'reconnect_protons',
                   'rb':'reconnect_stereo_dbond',
                   'rt':'reconnect_stereo_sp3',
                   'rm':'reconnect_stereo_sp3_inverted',
                   'rs':'reconnect_stereo_type',
                   'ii':'isotopic_atoms',
                   'ih':'isotopic_exchangable_H',
                   'ib':'isotopic_stereo_bond',
                   'it':'isotopic_stereo_sp3',
                   'im':'isotopic_stereo_sp3_inverted',
                   'is':'isotopic_stereo_type',
                   'ff':'fixedH_formula',
                   'fh':'fixedH_H_fixed',
                   'fq':'fixedH_charge',
                   'ft':'fixedH_stereo_sp3',
                   'fm':'fixedH_stereo_sp3_inverted',
                   'fs':'fixedH_stereo_type',
                   'fi':'fixedH_isotopic_atoms',
}


    def __init__(self, inchi):
        self.inchi = inchi
        self.parse_inchi(inchi = inchi)

    def __clearall__(self):
        self.massnumber = None
        self.stoichiometric_formula = None
        self.charge = None
        self.hydrogens = None
        self.dict_species = None
        self.atoms = None
        
    def __generate_dict_atomids__(self, formula):
        """
        Creates a dictionary with all atoms of the specie except all hydrogens (H, D, T)
        The key is an integer which can be used to identify the bonds/structure

        formula: stoichiometric formula of the skeleton. In most cases it is the stoichiometric
                 formula of the specie but in some cases protons have to be added or substracted
                 (e.g. H3O+)
        """

        # will contain a dictionary with ids of each atom except for hydrogens
        dict_atoms = {}
        # will contain the number of hydrogen atoms
        h_atoms = 0

        # find start position of new atom
        indices = [m.start() for m in re.finditer("[A-Z]", formula)]
        # append the length of the formula to the list to simplify splitting into different atoms
        indices.append(len(formula))
        # id - counter
        id = 1

        # split formula into different atoms
        for i in xrange(len(indices)-1):
            atoms = formula[indices[i]:indices[i+1]]
            # loop through all identical atoms
            found = re.search("[0-9]",atoms)
            if found is None:
                numberofatoms = 1
                atomsymbol = atoms
            else:
                numberofatoms = int(atoms[found.start():])
                atomsymbol = atoms[:found.start()]
            # hydrogens are not included into dictionary and only the number
            # of hydrogens will be returned
            if atomsymbol == 'H':
                h_atoms = numberofatoms
                continue
            for i in xrange(numberofatoms):
                dict_atoms[id] = {'symbol':atomsymbol, 'isotope_mass_diff':0}
                id += 1
        return dict_atoms, h_atoms


    def __parse_isotopic_layer__(self):
        """
        Parses the isotopic layer of the InChI and updates the dictionary of atoms and hydrogens accordingly
        """
        # initialize all isotopes with standard masses
        for atomid in self.atoms:
            atom = self.atoms[atomid]
            mass_reference = atom_mass_reference[atom['symbol']]
            atom['isotope'] = mass_reference 
            
        if not self.dict_species.has_key('isotopic_atoms'):
            return

        # parse isotopic layer and change isotopic mass number accordingly
        layers = self.dict_species['isotopic_atoms'].split(',')
        for layer in layers:

            if layer.find('D')>-1:
                # layer should have format aDn
                # a is the identification number of the atom to which they are attached
                # n is the number of these atoms attached to the (a)th atom, n=1 is ommited
                layer, num_atoms = layer.split('D')
                if num_atoms == '':
                    num_atoms = 1
                else:
                    num_atoms = int(num_atoms)
                found = re.search("[\+\-]", layer)
                if found:
                    atom_id = int(layer[:found.start()])
                else:
                    atom_id = int(layer)
                    layer = ''
                for hid in self.hydrogens:
                    if num_atoms > 0 and self.hydrogens[hid]['connected_to'] == [atom_id]:
                        self.hydrogens[hid]['massnumber'] = 2
                        self.hydrogens[hid]['isotope'] = 'D'                        
                        num_atoms -= 1                        
                
            elif layer.find('T')>-1:
                # layer should have format aDn
                # a is the identification number of the atom to which they are attached
                # n is the number of these atoms attached to the (a)th atom, n=1 is ommited
                layer, num_atoms = layer.split('T')
                if num_atoms == '':
                    num_atoms = 1
                else:
                    num_atoms = int(num_atoms)
                found = re.search("[\+\-]", layer)
                if found:
                    atom_id = int(layer[:found.start()])
                else:
                    atom_id = int(layer)
                    layer = ''
                for hid in self.hydrogens:
                    if num_atoms > 0 and self.hydrogens[hid]['connected_to'] == [atom_id]:
                        self.hydrogens[hid]['massnumber'] = 3
                        self.hydrogens[hid]['isotope'] = 'T'                        
                        num_atoms -= 1

                
            if layer == '':
                continue
            elif layer.find('+')>-1:
                atomid, isotope = layer.split('+')
                isotope = int(isotope)
            elif layer.find('-')>-1:
                atomid, isotope = layer.split('-')
                isotope = -int(isotope)
            else:
                print "Could not parse isotope info %s" % layer
                continue
            atom = self.atoms[int(atomid)]
            mass_reference = atom_mass_reference[atom['symbol']]
            atom['isotope_mass_diff'] = isotope
            atom['isotope'] = mass_reference + isotope
                                       #self.atoms[atomid]['isotope'] = isotope

        # process /h isotopic sublayer (isotopic information on mobile H atoms)
        if self.dict_species.has_key('isotopic_exchangable_H'):
            exchangableH = self.dict_species['isotopic_exchangable_H']
            found = re.search("[H,D,T][0-9]*",exchangableH)
            while found:
                isotope = exchangableH[found.start():found.end()]
                exchangableH = exchangableH[found.end():]
                found = re.search("[H,D,T][0-9]*",exchangableH)
                # if the number of replacements is just one, then 1 has been ommited
                if len(isotope)>1:
                    count_isotopes = int(isotope[1:])
                else:
                    count_isotopes = 1

                isotope = isotope[0]

                if isotope == 'D':
                    mass = 2
                elif isotope == 'T':
                    mass = 3
                else:
                    # if it is just hydrogen then nothing has to be done
                    continue
                # replace first all the mobile hydrogens
                for hydrogen in self.hydrogens:
                    # if all hydrogens have been replaced then stop replacements
                    if count_isotopes == 0:
                        break
                    # check if it has been replaced already
                    if self.hydrogens[hydrogen]['massnumber'] != 1:
                        continue
                    if len(self.hydrogens[hydrogen]['connected_to'])>1:
                        self.hydrogens[hydrogen]['isotope'] = isotope
                        self.hydrogens[hydrogen]['massnumber'] = mass
                        count_isotopes -= 1

                # replace then normal hydrogens in the order of occurances
                for hydrogen in self.hydrogens:
                    # if all hydrogens have been replaced then stop replacements
                    if count_isotopes == 0:
                        break
                    # check if it has been replaced already
                    if self.hydrogens[hydrogen]['massnumber'] != 1:
                        continue

                    self.hydrogens[hydrogen]['isotope'] = isotope
                    self.hydrogens[hydrogen]['massnumber'] = mass
                    count_isotopes -= 1
                                       

    def __parse_charge__(self):
        """
        Parses the main charge layer. 
        """

        self.dict_species['totalcharge'] = 0
        if not self.dict_species.has_key('charge'):
            return
        
        for q in self.dict_species['charge'].split(";"):
            if q != "":
                self.dict_species['totalcharge'] += int(q)
                
    def __parse_protons__(self):
        """
        Determines the number of additional protons from the inchi
        """

        self.dict_species['num_protons'] = 0
        if not self.dict_species.has_key('protons'):
            return
        
        for q in self.dict_species['protons'].split(";"):
            if q != "":
                self.dict_species['num_protons'] += int(q)

    def __parse_hydrogen_layer__(self):
        """
        The hyrdogne layer contains the information how many hydrogens are connected to each atom
        example: 1H2 means 2 hydrogens are connected to atom 1
                 1,3H2 means 2 hydrogens are connected to atom1 and 2 to atom 3
                 1-3H2 means 2 hydrogens are connected to atom 1, 2 to atom 2 and 2 to atom 3
                 (H2, 1,3) means 2 hydrogens are mobile and migrate between atom 1 and 3 (2 hydrogens in total)
        """
        # first hydrogen info which is enclosed in brackets have to be identified
        # otherwise a split by ',' will not work
        if not self.dict_species.has_key('H_atoms'):
            self.dict_species['H_atoms'] = ""
            
        hlayer = self.dict_species['H_atoms']

        hydrogenlist = {}
        h_id = 1
        while hlayer.find('(')!=-1:
            left = hlayer.find('(')
            right = hlayer.find(')')
            # add info to a list
            mobileH = hlayer[left+1:right].split(',')
            atomids = [int(id) for id in mobileH[1:]]
            if mobileH[0]=='H':
                count_H = 1
            else:
                count_H = int(mobileH[0][1:])
            for i in xrange(count_H):
                hydrogenlist[h_id] = {'isotope':'H', 'massnumber': 1,'connected_to':atomids}
                h_id += 1
                
            # remove info from the string
            hlayer = hlayer.replace(hlayer[left:right+1],'')
            
        layers = [i for i in hlayer.split(',') if i!='']
        last_layer = ''
        for layer in layers:
            # there might be a kommata before the first occurance of 'H'
            # which belongs to a list of atoms to which H are connected
            layer = last_layer+','+layer
            if layer.find('H') == -1:
                # ignore this splitting and merge the result with next loop
                last_layer = layer
                continue
            else:
                last_layer = ''
            
            # layer contains aHn (a is id of the connected atom, n is the number of hydrogens connected
            atomids, count_H = layer.split('H')
            id_range = atomids.split('-')
            if len(id_range) == 2:
                id_range = range(int(atomids.split('-')[0]), int(atomids.split('-')[1])+1)
            else:
                id_range = [int(id) for id in id_range[0].split(',') if id!='']
            if count_H == '':
                count_H = 1
            else:
                count_H = int(count_H)
            for atomid in id_range:
                for i in xrange(count_H):
                    hydrogenlist[h_id] = {'isotope':'H', 'massnumber': 1,'connected_to':[atomid]}
                    h_id += 1

        # if less H atoms are in the list of hydrogens than expected from the formula specified in the InChI
        # then the remaining H atoms have to be added to the skeleton (atomids)
        if len(hydrogenlist) < self.dict_species['num_H_atoms']:
            for i in xrange(self.dict_species['num_H_atoms'] - len(hydrogenlist)):
                self.atoms[len(self.atoms)+1+i] = {'isotope': 1, 'symbol': 'H', 'isotope_mass_diff' : 0}

        # add protons (to the end of the list)
        if self.dict_species['num_protons']>0:
            for i in xrange(self.dict_species['num_protons']):
                hydrogenlist[h_id] =  {'isotope':'H', 'massnumber': 1, 'charge': '1', 'connected_to':[]}
                h_id += 1

        # remove protons (from the end of the list)
        if self.dict_species['num_protons']<0:
            for i in xrange(abs(self.dict_species['num_protons'])):
                h_id -= 1
                hydrogen = hydrogenlist.pop(h_id)
                # put a charge to the first atom to which it was connected
                self.atoms[hydrogen['connected_to'][0]]['charge'] = -1

        self.hydrogens = hydrogenlist

    def __get_charge__(self):
        self.__parse_charge__()
        self.__parse_protons__()

        # each proton adds a charge of +1 to the total charge
        self.charge = self.dict_species['totalcharge'] + self.dict_species['num_protons']

    def __generate_stoichiometric_formula__(self):
        """
        Creates the stoichiometric formula from the main and the charge layer 
        """

        # create the string which contains the charge info in the stoichiometric formula e.g. '+', '-2', '+3'
        charge_str = ''
        if self.charge > 0:
            charge_str = "+"
        elif self.charge < 0:
            charge_str = "-"
       
        if abs(self.charge) > 1:
            charge_str += "%d" % abs(charge)
        
        # create dictionary with number of each atom
        dict_atom_count = {}
        for atomid in self.atoms:
            if not dict_atom_count.has_key(self.atoms[atomid]['symbol']):
                dict_atom_count[self.atoms[atomid]['symbol']] = 1
            else:
                dict_atom_count[self.atoms[atomid]['symbol']] += 1
                               
        # calculate number of hydrogens (include protons) and add them to the dict
        count_hydrogens = self.dict_species['num_H_atoms'] + self.dict_species['num_protons']
        if count_hydrogens > 0:
            dict_atom_count['H'] = count_hydrogens

        # create the string which contains the atom info in Hill's notation (alphabetic order)
        self.stoichiometric_formula = ""
        for atom in sorted(dict_atom_count):
            self.stoichiometric_formula += atom
            if dict_atom_count[atom]>1:
                self.stoichiometric_formula += "%d" % dict_atom_count[atom]

        # combine atom- and charge-info
        self.stoichiometric_formula += "%s" % charge_str

    def __get_massnumber__(self):
        """
        Determines the mass number from the atom dict and the hydrogen dict
        """
        self.massnumber = 0
        for id in self.atoms:
            self.massnumber += self.atoms[id]['isotope']
        for id in self.hydrogens:
            self.massnumber += self.hydrogens[id]['massnumber']

    def __add_hydrogens2atoms__(self):
        """
        Add the hydrogens to the dictionary of atoms. Hydrogens have been removed from the list
        in the InChI
        """
        atom_length = len(self.atoms)
        for id in self.hydrogens:
            if self.hydrogens[id].has_key('charge'):
                self.atoms[int(id)+atom_length] = {'isotope': self.hydrogens[id]['massnumber'],
                                                   'symbol': 'H',
                                                   'charge': self.hydrogens[id]['charge'],
                                                   }
            else:
                self.atoms[int(id)+atom_length] = {'isotope': self.hydrogens[id]['massnumber'],
                                                   'symbol': 'H',
                                                   }
        
    def parse_inchi(self, inchi):
        """
        Parses the InChI.
        """
        # make sure old values will be overwritten
        self.__clearall__()
        self.inchi = inchi
        
        # will contain a dictionary of return values    
        self.dict_species = {}

        # generate list of layers
        layers = inchi.split("/")

        # fist layer defines if inchi is standard
        if layers[0] == "1S":
            self.dict_species['standard_inchi'] = True
        else:
            self.dict_species['standard_inchi'] = False

        init_layer = 1 # start processing with this layer
        # second layer specifies stoichiometric formula in Hill's notation
        if layers[1][0].upper() == layers[1][0]:
            self.dict_species['formula'] = layers[1]
            init_layer += 1
        else:
            self.dict_species['formula'] = ""
            
        self.dict_species['atomids'], self.dict_species['num_H_atoms'] = self.__generate_dict_atomids__(self.dict_species['formula'])
        self.atoms = self.dict_species['atomids']
            
        # loop through all the layers
        layer_str = ''
        for layer in layers[init_layer:]:
            # connection layer
            # there are two different '/h'-layers, one before and one after the '/i' isotopic
            # layer. Both have different meanings!!! As far as I understand the second one
            # contains additonal information for fixed hydrogens (or D,T) (isotopic info for hydrogens)

            # isotopic layer begins with sublayer i
            if layer[0] == 'i':
                layer_str = 'i'
            # fixed_H layer begins with sublayer f (only present if non-standard inchi)
            if layer[0] == 'f':
                layer_str = 'f'
                
            self.dict_species[self.dict_layers["%s%s" % (layer_str, layer[0])]] = layer[1:]

        # parse layer with charge and proton information
        self.__get_charge__()
        # parse main layer with hydrogen information
        self.__parse_hydrogen_layer__()
        # parse layer with istotopic information 
        self.__parse_isotopic_layer__()
        # create the stoichiometric formula
        self.__generate_stoichiometric_formula__()
        # get the massnumber
        self.__get_massnumber__()
        # create a dictionary with all atoms including hydrogens
        self.__add_hydrogens2atoms__()

