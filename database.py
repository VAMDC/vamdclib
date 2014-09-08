# -*- coding: utf-8 -*-
import sqlite3
from datetime import datetime
from dateutil import parser

import functions
import query as q
import results
import request as r
import nodes
import specmodel
from settings import *

# List of Temperatures for which the Partitionfunction is stored in the sqlite database.
Temperatures = [1.072, 1.148, 1.230, 1.318, 1.413, 1.514, 1.622, 1.738, 1.862, 1.995, 2.138, 2.291, 2.455, 2.630, 2.725, 2.818, 3.020, 3.236, 3.467, 3.715, 3.981, 4.266, 4.571, 4.898, 5.000, 5.248, 5.623, 6.026, 6.457, 6.918, 7.413, 7.943, 8.511, 9.120, 9.375, 9.772, 10.471, 11.220, 12.023, 12.882, 13.804, 14.791, 15.849, 16.982, 18.197, 18.750, 19.498, 20.893, 22.387, 23.988, 25.704, 27.542, 29.512, 31.623, 33.884, 36.308, 37.500, 38.905, 41.687, 44.668, 47.863, 51.286, 54.954, 58.884, 63.096, 67.608, 72.444, 75.000, 77.625, 83.176, 89.125, 95.499, 102.329, 109.648, 117.490, 125.893, 134.896, 144.544, 150.000, 154.882, 165.959, 177.828, 190.546, 204.174, 218.776, 225.000, 234.423, 251.189, 269.153, 288.403, 300.000, 309.030, 331.131, 354.813, 380.189, 407.380, 436.516, 467.735, 500.000, 501.187, 537.032, 575.440, 616.595, 660.693, 707.946, 758.578, 812.831, 870.964, 933.254, 1000.000, ]

#DATABASE_FILE = "cdms_sqlite.db"
##========================================================================
class Database(object):
    """
    An instance of Database contains methods to store data obtained from VAMDC nodes
    in an sqlite database.

    :ivar conn: connection handler to the sqlite database
    """
    ##********************************************************************
    def __init__(self, database_file = DATABASE_FILE):
        """
        Connect to database.

        Database will be created if it does not exist
        """
        try:
            self.conn = sqlite3.connect(database_file)
        except sqlite3.Error, e:
            print " "
            print "Can not connect to sqlite3 databse %s." % database_file
            print "Error: %d: %s" % (e.args[0], e.args[1])
        return

    ##********************************************************************
    def create_structure(self):
        """
        Create tables in the sqlite3 database

        Tables which will be created:
        - Partitionfunctions
        - Transitions
        """

        cursor = self.conn.cursor()
        #----------------------------------------------------------
        # drop tables if they exist
        stmts = ("DROP TABLE IF EXISTS Partitionfunctions;",
                 "DROP TABLE IF EXISTS Transitions;",)

        for stmt in stmts:
            cursor.execute(stmt)
        #----------------------------------------------------------


        #-------------------------------------------------
        # INSERT TRANSITIONS

        sql_create_transitions = """CREATE TABLE Transitions (
        T_Name TEXT,
        T_Frequency REAL,
        T_Intensity REAL,
        T_EinsteinA REAL,
        T_Uncertainty REAL,
        T_EnergyLower REAL,
        T_UpperStateDegeneracy INTEGER,
        T_NuclearSpinIsomer TEXT,
        T_HFS TEXT,
        T_Case TEXT,
        T_UpperStateQuantumNumbers TEXT,
        T_LowerStateQuantumNumbers TEXT) """


        sql_create_partitionfunctions = """ CREATE TABLE Partitionfunctions (
        PF_Name TEXT,
        PF_VamdcSpeciesID TEXT,
        PF_SpeciesID TEXT,
        PF_NuclearSpinIsomer TEXT,
        PF_HFS TEXT,
        PF_1_072 REAL,
        PF_1_148 REAL,
        PF_1_230 REAL,
        PF_1_318 REAL,
        PF_1_413 REAL,
        PF_1_514 REAL,
        PF_1_622 REAL,
        PF_1_738 REAL,
        PF_1_862 REAL,
        PF_1_995 REAL,
        PF_2_138 REAL,
        PF_2_291 REAL,
        PF_2_455 REAL,
        PF_2_630 REAL,
        PF_2_725 REAL,
        PF_2_818 REAL,
        PF_3_020 REAL,
        PF_3_236 REAL,
        PF_3_467 REAL,
        PF_3_715 REAL,
        PF_3_981 REAL,
        PF_4_266 REAL,
        PF_4_571 REAL,
        PF_4_898 REAL,
        PF_5_000 REAL,
        PF_5_248 REAL,
        PF_5_623 REAL,
        PF_6_026 REAL,
        PF_6_457 REAL,
        PF_6_918 REAL,
        PF_7_413 REAL,
        PF_7_943 REAL,
        PF_8_511 REAL,
        PF_9_120 REAL,
        PF_9_375 REAL,
        PF_9_772 REAL,
        PF_10_471 REAL,
        PF_11_220 REAL,
        PF_12_023 REAL,
        PF_12_882 REAL,
        PF_13_804 REAL,
        PF_14_791 REAL,
        PF_15_849 REAL,
        PF_16_982 REAL,
        PF_18_197 REAL,
        PF_18_750 REAL,
        PF_19_498 REAL,
        PF_20_893 REAL,
        PF_22_387 REAL,
        PF_23_988 REAL,
        PF_25_704 REAL,
        PF_27_542 REAL,
        PF_29_512 REAL,
        PF_31_623 REAL,
        PF_33_884 REAL,
        PF_36_308 REAL,
        PF_37_500 REAL,
        PF_38_905 REAL,
        PF_41_687 REAL,
        PF_44_668 REAL,
        PF_47_863 REAL,
        PF_51_286 REAL,
        PF_54_954 REAL,
        PF_58_884 REAL,
        PF_63_096 REAL,
        PF_67_608 REAL,
        PF_72_444 REAL,
        PF_75_000 REAL,
        PF_77_625 REAL,
        PF_83_176 REAL,
        PF_89_125 REAL,
        PF_95_499 REAL,
        PF_102_329 REAL,
        PF_109_648 REAL,
        PF_117_490 REAL,
        PF_125_893 REAL,
        PF_134_896 REAL,
        PF_144_544 REAL,
        PF_150_000 REAL,
        PF_154_882 REAL,
        PF_165_959 REAL,
        PF_177_828 REAL,
        PF_190_546 REAL,
        PF_204_174 REAL,
        PF_218_776 REAL,
        PF_225_000 REAL,
        PF_234_423 REAL,
        PF_251_189 REAL,
        PF_269_153 REAL,
        PF_288_403 REAL,
        PF_300_000 REAL,
        PF_309_030 REAL,
        PF_331_131 REAL,
        PF_354_813 REAL,
        PF_380_189 REAL,
        PF_407_380 REAL,
        PF_436_516 REAL,
        PF_467_735 REAL,
        PF_500_000 REAL,
        PF_501_187 REAL,
        PF_537_032 REAL,
        PF_575_440 REAL,
        PF_616_595 REAL,
        PF_660_693 REAL,
        PF_707_946 REAL,
        PF_758_578 REAL,
        PF_812_831 REAL,
        PF_870_964 REAL,
        PF_933_254 REAL,
        PF_1000_000 REAL,
        PF_ResourceID TEXT,
        PF_URL TEXT,
        PF_Comment TEXT,
        PF_Timestamp)"""

        sql_create_idx_pfname = "CREATE INDEX 'IDX_PF_Name' ON Partitionfunctions (PF_Name);"
        sql_create_idx_tname = "CREATE INDEX 'IDX_T_Name' ON Transitions (T_Name, T_Frequency, T_EnergyLower);"
        sql_create_idx_freq = "CREATE INDEX 'IDX_T_Frequency' ON Transitions (T_Frequency, T_EnergyLower);"

        cursor.execute(sql_create_transitions)
        cursor.execute(sql_create_partitionfunctions)
        cursor.execute(sql_create_idx_pfname)
        cursor.execute(sql_create_idx_tname)
        cursor.execute(sql_create_idx_freq)
        #-------------------------------------------------------------

        return
    

    ##********************************************************************
    def check_for_updates(self, node):
        """
        """

        count_updates = 0
        counter = 0
        #species_list = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, datetime(PF_Timestamp) FROM Partitionfunctions ")
        rows = cursor.fetchall()
        num_rows = len(rows)
        query = q.Query()
        request = r.Request()

        for row in rows:
            counter += 1
            print "%5d/%5d: Check specie %-55s (%-15s): " % (counter, num_rows, row[0], row[1]),
            #id = row[1]
            vamdcspeciesid = row[2]
#            query_string = "SELECT ALL WHERE VAMDCSpeciesID='%s'" % vamdcspeciesid
            query_string = "SELECT ALL WHERE SpeciesID=%s" % row[1][6:]
            request.setquery(query_string)
            request.setnode(node)

            try:
                changedate = request.getlastmodified()
            except timeout:
                print "TIMEOUT"
            except Exception, e:
                print "Error in getlastmodified: %s " % e.strerror
                changedate = None

            tstamp = parser.parse(row[3] + " GMT")
            if changedate is None:
                print " -- UNKNOWN (Could not retrieve information)"
                continue
            if tstamp < changedate:
                print " -- UPDATE AVAILABLE "
                count_updates += 1
            else:
                print " -- up to date"

        if count_updates == 0:
            print "\r No updates for your entries available"
        print "Done"

    ##********************************************************************
    def check_for_new_species(self, node):
        """
        """

        counter = 0
        cursor = self.conn.cursor()

        request = r.Request(node = node)
        result = request.getspecies()
                
        for id in result.data['Molecules']:
            try:
                cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Timestamp FROM Partitionfunctions WHERE PF_SpeciesID=?", [(id)])
                exist = cursor.fetchone()
                if exist is None:
                    print "ID: %s" % result.data['Molecules'][id]
                    counter += 1
            except Exception, e:
                print e
                print id
        print "There are %d new species available" % counter

    ##********************************************************************
    def show_species(self):
        """
        Lists all species stored in the database
        """
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Timestamp FROM Partitionfunctions")
        rows = cursor.fetchall()
        for row in rows:
            print "%-10s %-60s %20s %s" % (row[1], row[0], row[2], row[3])


    ##********************************************************************
    def delete_species(self, speciesid):
        """
        Deletes species stored in the database

        speciesid: Id of the Specie
        """
        deleted_species = []
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name FROM Partitionfunctions WHERE PF_SpeciesID = ?", (speciesid, ))
        rows = cursor.fetchall()
        for row in rows:
            deleted_species.append(row[0])
            cursor.execute("DELETE FROM Transitions WHERE T_Name = ?", (row[0], ))
            cursor.execute("DELETE FROM Partitionfunctions WHERE PF_Name = ?", (row[0], ))
        return deleted_species

    ##********************************************************************
    def insert_species_data(self, species, node, update=False):
        """
        Inserts new species into the local database

        species: species which will be inserted
        node:    vamdc-node / type: instance(nodes.node)
        update:  if True then all entries in the local database with the same
                 species-id will be deleted before the insert is performed.
        """

        # create a list of names. New names have not to be in that list
        names_black_list = []
        
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name FROM Partitionfunctions")
        rows = cursor.fetchall()
        for row in rows:
            names_black_list.append(row[0])

        #----------------------------------------------------------
        # Create a list of species for which transitions will be
        # retrieved and inserted in the database.
        # Species have to be in the Partitionfunctions - table

        if not functions.isiterable(species):
            species = [species]

        #--------------------------------------------------------------

        for specie in species:
            # if species is a dictionary (e.g. specmodel.Molecules)
            # then get the species-instance instead of only the key.
            if isinstance(species, dict):
                specie = species[specie]
                
            num_transitions = {}
            # will contain a list of names which belong to one specie
            species_names = {}
            # list will contain species whose insert-failed
            species_with_error = []

            # check if specie is of type Molecule
            if isinstance(specie, specmodel.Molecule):
                speciesid = specie.SpeciesID
                vamdcspeciesid = specie.VAMDCSpeciesID
                formula = specie.OrdinaryStructuralFormula
            if isinstance(specie, specmodel.Atom):
                speciesid = specie.SpeciesID
                vamdcspeciesid = specie.VAMDCSpeciesID
#                formula = specie.OrdinaryStructuralFormula
            else:
                try:
                    if isinstance(specie, str) and len(specie) == 27:
                        vamdcspeciesid = specie
                        speciesid = None
                except:
                    print "Specie is not of wrong type"
                    print "Type Molecule or string (Inchikey) is allowed"
                    continue
            if speciesid:
                print "Processing: {speciesid}".format(speciesid = speciesid)
            else:
                print "Processing: {vamdcspeciesid}".format(vamdcspeciesid = vamdcspeciesid)
                

            try:
                # Create query string
                query_string = "SELECT ALL WHERE VAMDCSpeciesID='%s'" % vamdcspeciesid
                request = r.Request()

                # Get data from the database
                request.setnode(node)
                request.setquery(query_string)

                result = request.dorequest()
                #result.populate_model()
            except Exception, e:
                print " -- Error %s: Could not fetch and process data" % e.strerror
                continue    
            #---------------------------------------

            cursor = self.conn.cursor()
            cursor.execute('BEGIN TRANSACTION')

            #------------------------------------------------------------------------------------------------------
            # if update is allowed then all entries in the database for the given species-id will be
            # deleted, and thus replaced by the new data
            if update:
                if speciesid is None:
                    for sid in result.data['Molecules'].keys() + result.data['Atoms'].keys():
                        deleted_species = self.delete_species(sid)
                        for ds in deleted_species:
                            names_black_list.remove(ds)
                else:
                    deleted_species = self.delete_species(speciesid)
                    for ds in deleted_species:
                        names_black_list.remove(ds)

            #------------------------------------------------------------------------------------------------------
            
            #------------------------------------------------------------------------------------------------------
            # Insert all transitions
            num_transitions_found = len(result.data['RadiativeTransitions'])
            counter_transitions = 0
            for trans in result.data['RadiativeTransitions']:
                counter_transitions+=1
                print "\r insert transition %d of %d" % (counter_transitions, num_transitions_found),
                # data might contain transitions for other species (if query is based on ichikey/vamdcspeciesid).
                # Insert transitions only if they belong to the correct specie

                if result.data['RadiativeTransitions'][trans].SpeciesID == speciesid or speciesid is None:
                    id = str(result.data['RadiativeTransitions'][trans].SpeciesID)
                    # if an error has occured already then there will be no further insert
                    if id in species_with_error:
                        continue

                    # Get upper and lower state from the states table
                    try:
                        upper_state = result.data['States']["%s" % result.data['RadiativeTransitions'][trans].UpperStateRef]
                        lower_state = result.data['States']["%s" % result.data['RadiativeTransitions'][trans].LowerStateRef]
                    except (KeyError, AttributeError):
                        print " -- Error: State is missing"
                        species_with_error.append(id)
                        continue

                    if id in result.data['Atoms'].keys():
                        is_atom = True
                        is_molecule = False
                        atomname = self.createatomname(result.data['Atoms'][id])
                    elif id in result.data['Molecules'].keys():
                        is_atom = False
                        is_molecule = True
                        formula = str(result.data['Molecules'][id].OrdinaryStructuralFormula)

                        # Get string which identifies the vibrational states involved in the transition
                        t_state = self.getvibstatelabel(upper_state, lower_state)
                        
                    else:
                        continue
                                                
                    # Get hyperfinestructure info if hfsInfo is None
                    # only then the hfsInfo has not been inserted in the species name
                    # (there can be multiple values in the complete dataset
                    t_hfs = ''
                    try:
                        for pc in result.data['RadiativeTransitions'][trans].ProcessClass:
                            if str(pc)[:3] == 'hyp':
                                t_hfs = str(pc)
                    except Exception, e:
                            print "Error: %s", e

                    frequency = float(result.data['RadiativeTransitions'][trans].FrequencyValue)
                    try:
                        uncertainty = "%lf" % float(result.data['RadiativeTransitions'][trans].FrequencyAccuracy)
                    except TypeError:
                        print " -- Error uncertainty not available"
                        species_with_error.append(id)
                        continue

                    # Get statistical weight if present
                    try:
                        weight = int(upper_state.TotalStatisticalWeight)
                    except:
                        print " -- Error statistical weight not available"
                        species_with_error.append(id)
                        continue

                    # Get nuclear spin isomer (ortho/para) if present
                    try:
                        nsiName = upper_state.NuclearSpinIsomerName
                    except AttributeError:
                        nsiName = None

                    # if nuclear spin isomer is defined then two entries have to be generated
                    if nsiName is not None and nsiName != '':
                        nsinames = [nsiName, None]
                        nsiStateOrigin = result.data['States']["%s" % upper_state.NuclearSpinIsomerLowestEnergy]
                        nsiEnergyOffset = float(nsiStateOrigin.StateEnergyValue)
                    else:
                        nsinames = [None]

                    for nsiName in nsinames:
                        # create name
                        if is_atom == True:
                            t_name = atomname
                        else:
                            t_affix = ";".join([affix for affix in [t_hfs, nsiName] if affix is not None and affix!=''])
                            t_name = "%s;%s;%s" % (formula, t_state, t_affix)
                        t_name = t_name.strip()
                        # remove all blanks in the name
                        t_name = t_name.replace(' ','')
                        # check if name is in the list of forbidden names and add counter if so
                        i = 1
                        while t_name in names_black_list:
                            t_name = "%s#%d" % (t_name.split('#')[0], i)
                            i += 1
                        # update list of distinct species names.
                        if id in species_names:
                            if not t_name in species_names[id]:
                                species_names[id].append(t_name)
                                num_transitions[t_name] = 0
                        else:
                            species_names[id] = [t_name]
                            num_transitions[t_name] = 0

                        if nsiName is not None:
                            lowerStateEnergy = float(lower_state.StateEnergyValue) - nsiEnergyOffset
                        else:
                            lowerStateEnergy = float(lower_state.StateEnergyValue)
                            
                        
                        # Insert transition into database
                        try:
                            cursor.execute("""INSERT INTO Transitions (
                            T_Name,
                            T_Frequency,
                            T_EinsteinA,
                            T_Uncertainty,
                            T_EnergyLower,
                            T_UpperStateDegeneracy,
                            T_HFS,
                            T_UpperStateQuantumNumbers,
                            T_LowerStateQuantumNumbers) VALUES
                            (?, ?,?,?,?, ?,?, ?,?)""",
                                           (t_name,
                                            "%lf" % frequency,
                                            "%g" % float(result.data['RadiativeTransitions'][trans].TransitionProbabilityA),
                                            uncertainty, "%lf" % lowerStateEnergy,
                                            weight,
                                            #upper_state.QuantumNumbers.case,
                                            t_hfs,
                                            str(upper_state.QuantumNumbers.qn_string),
                                            str(lower_state.QuantumNumbers.qn_string),
                                            ))
                            num_transitions[t_name] += 1
                        except Exception, e:
                            print "Transition has not been inserted:\n Error: %s" % e
            print "\n"
            #------------------------------------------------------------------------------------------------------

            #------------------------------------------------------------------------------------------------------
            # delete transitions for all entries where an error occured during the insert
            for id in species_with_error:
                print " -- Species {id} has not been inserted due to an error ".format(id=str(id))
                try:
                    for name in species_names[id]:
                        cursor.execute("DELETE FROM Transitions WHERE T_Name=?", (str(name),))
                        print " --    {name} ".format(name=str(name))
                except:
                    pass

            #------------------------------------------------------------------------------------------------------
            # insert specie in Partitionfunctions (header) table
            if node:
                resourceID = node.identifier
                url = node.url
            else:
                resourceID = 'NULL'
                url = 'NULL'
                

            # Insert molecules
            for id in species_names:
                if id in species_with_error:
                    continue
                for name in species_names[id]:
                    # determine hyperfine-structure affix and nuclear spin isomer affix
                    try:
                        hfs = ''
                        nsi = ''
                        for affix in name.split("#")[0].split(';',2)[2].split(";"):
                            if affix.strip()[:3] == 'hyp':
                                hfs = affix.strip()
                            else:
                                # if affix does not identify hyperfine structure
                                # it identifies the nuclear spin isomer
                                nsi = affix.strip()
                    except:
                        hfs = ''

                    # Insert row in partitionfunctions
                    try:
                        if id in result.data['Atoms']:
                            if not result.data['Atoms'][id].__dict__.has_key('Comment'):
                                result.data['Atoms'][id].Comment = ""
                            cursor.execute("INSERT INTO Partitionfunctions (PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Comment, PF_ResourceID, PF_URL, PF_Timestamp) VALUES (?,?,?,?,?,?,?)",
                                           ("%s" % name,
                                            id,
                                            "%s" % (result.data['Atoms'][id].VAMDCSpeciesID),
                                            "%s" % (result.data['Atoms'][id].Comment),
                                            resourceID,
                                            "%s%s%s" % (url, "sync?LANG=VSS2&amp;REQUEST=doQuery&amp;FORMAT=XSAMS&amp;QUERY=Select+*+where+SpeciesID%3D", id),
                                            datetime.now(), ))
                        else:
                            cursor.execute("INSERT INTO Partitionfunctions (PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_HFS, PF_NuclearSpinIsomer, PF_Comment, PF_ResourceID, PF_URL, PF_Timestamp) VALUES (?,?,?,?,?,?,?,?,?)",
                                           ("%s" % name,
                                            id,
                                            "%s" % (result.data['Molecules'][id].VAMDCSpeciesID),
                                            hfs,
                                            nsi, 
                                            "%s" % (result.data['Molecules'][id].Comment),
                                            resourceID,
                                            "%s%s%s" % (url, "sync?LANG=VSS2&amp;REQUEST=doQuery&amp;FORMAT=XSAMS&amp;QUERY=Select+*+where+SpeciesID%3D", id),
                                            datetime.now(), ))
                    except sqlite3.Error as e:
                        print "An error occurred:", e.args[0]
                    except Exception as e:
                        print "An error occurred:", e.args[0]
                        print result.data['Molecules'].keys()

                # Update Partitionfunctions
                if id in result.data['Atoms'].keys():
                    for temperature in Temperatures:
                        pf_values = specmodel.calculate_partitionfunction(result.data['States'], temperature = temperature)
                        try:
                            field = ("PF_%.3lf" % float(temperature)).replace('.', '_')
                            sql = "UPDATE Partitionfunctions SET %s=? WHERE PF_SpeciesID=? " % field
                            cursor.execute(sql, (pf_values[id], id))
                        except Exception, e:
                            print "SQL-Error: %s " % sql
                            print pf_value, id
                            print "Error: %d: %s" % (e.args[0], e.args[1])
                else:
                    try:
                        for pfs in result.data['Molecules'][id].PartitionFunction:
                            if not pfs.__dict__.has_key('NuclearSpinIsomer'):
                                nsi = ''
                            else:
                                nsi = pfs.NuclearSpinIsomer  
                            for temperature in pfs.values.keys():

                                try:
                                    field = ("PF_%.3lf" % float(temperature)).replace('.', '_')
                                    sql = "UPDATE Partitionfunctions SET %s=? WHERE PF_SpeciesID=? AND IFNULL(PF_NuclearSpinIsomer,'')=?" % field
                                    cursor.execute(sql, (pfs.values[temperature], id, nsi))
                                except Exception, e:
                                    print "SQL-Error: %s " % sql
                                    print pfs.values[temperature], id
                                    print "Error: %d: %s" % (e.args[0], e.args[1])
                    except:
                        pass
            #------------------------------------------------------------------------------------------------------

            for row in num_transitions:
                print "      for %s inserted %d transitions" % (row, num_transitions[row])
            self.conn.commit()
            cursor.close()

    ##********************************************************************
    def update_database(self, add_nodes = None, insert_only = False, update_only = False):
        """
        Checks if there are updates available for all entries. Updates will
        be retrieved from the resource specified in the database.
        All resources will be searched for new entries, which will be inserted
        if available. Additional resources can be specified via add_nodes.

        add_nodes: Single or List of node-instances (nodes.Node)
        """
        # counter to identify which entry is currently processed
        counter = 0
        # counter to count available updates
        count_updates = 0
        # list of database - nodes which are currently in the local database
        dbnodes = []
        # create an instance with all available vamdc-nodes
        nl = nodes.Nodelist()

        # attach additional nodes to the list of dbnodes (for insert)
        if not functions.isiterable(add_nodes):
            add_nodes = [add_nodes]
        for node in add_nodes:
            if node is None:
                pass
            elif not isinstance(node, nodes.Node):
                print "Could not attach node. Wrong type, it should be type <nodes.Node>"
            else:
                dbnodes.append(node)
        
        #--------------------------------------------------------------------
        # Check if updates are available for entries

        # Get list of species in the database
        cursor = self.conn.cursor()
        cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, datetime(PF_Timestamp), PF_ResourceID FROM Partitionfunctions ")
        rows = cursor.fetchall()
        num_rows = len(rows)
        query = q.Query()
        request = r.Request()

        if not insert_only:
            print("----------------------------------------------------------")
            print "Looking for updates"
            print("----------------------------------------------------------")

            for row in rows:
                counter += 1
                print "%5d/%5d: Check specie %-55s (%-15s): " % (counter, num_rows, row[0], row[1]),
                try:
                    node = nl.getnode(str(row[4]))
                except:
                    node = None
                if node is None:
                    print " -- RESOURCE NOT AVAILABLE"
                    continue
                else:
                    if node not in dbnodes:
                        dbnodes.append(node)

                vamdcspeciesid = row[2]
                # Currently the database prefix XCDMS- or XJPL- has to be removed
                speciesid = row[1].split("-")[1]
                query_string = "SELECT ALL WHERE SpeciesID=%s" % speciesid
                request.setnode(node)
                request.setquery(query_string)

                errorcode = None
                try:
                    changedate = request.getlastmodified()
#                except r.TimeOutError, e:
#                    errorcode = e.strerror
#                    changedate = None
                except Exception, e:
                    errorcode = e.strerror
                    changedate = None

                tstamp = parser.parse(row[3] + " GMT")
                if changedate is None:
                    if errorcode is None:
                        errorcode = "UNKNOWN"
                    print " -- %s (Could not retrieve information)" % errorcode
                    continue
                if tstamp < changedate:
                    print " -- UPDATE AVAILABLE "
                    count_updates += 1
                    print " -- PERFORM UPDATE -- "
                    query_string = "SELECT SPECIES WHERE SpeciesID=%s" % speciesid
                    request.setquery(query_string)

                    result = request.dorequest()
                    try:
                        result.populate_model()
                    except:
                        print " Error: Could not process data "
                        continue
                    try:
                        self.insert_species_data(result.data['Molecules'], node, update = True)
                    except:
                        print " Error: Could not update data "
                        continue
                    print " -- UPDATE DONE    -- "
                else:
                    print " -- up to date"

            if count_updates == 0:
                print "\r No updates for your entries available"
            print "Done"
        else:
            cursor.execute("SELECT distinct PF_ResourceID FROM Partitionfunctions ")
            rows = cursor.fetchall()
            for row in rows:
                try:
                    node = nl.getnode(str(row[0]))
                except:
                    node = None
                if node is None:
                    print " -- RESOURCE NOT AVAILABLE"
                    continue
                else:
                    if node not in dbnodes:
                        dbnodes.append(node)


        if update_only:
            return
        
        # Check if there are new entries available

        #---------------------------------------------------------
        # Check all dbnodes for new species
        for node in dbnodes:
            counter = 0
            insert_molecules_list = []
            print("----------------------------------------------------------")
            print "Query '{dbname}' for new species ".format(dbname=node.name)
            print("----------------------------------------------------------")
            request.setnode(node)
            result = request.getspecies()
            for id in result.data['Molecules']:
                try:
                    cursor.execute("SELECT PF_Name, PF_SpeciesID, PF_VamdcSpeciesID, PF_Timestamp FROM Partitionfunctions WHERE PF_SpeciesID=?", [(id)])
                    exist = cursor.fetchone()
                    if exist is None:
                        print "   %s" % result.data['Molecules'][id]
                        insert_molecules_list.append(result.data['Molecules'][id])
                        counter += 1
                except Exception, e:
                    print e
                    print id
            print "There are %d new species available" % counter
            print("----------------------------------------------------------")
            print "Start insert"
            print("----------------------------------------------------------")           
            self.insert_species_data(insert_molecules_list, node)
            print("----------------------------------------------------------")           
            print "Done"

    ##********************************************************************
    def getvibstatelabel(self, upper_state, lower_state):
        """
        create a vibrational state label for a transition
        in:
           upper_state = state instance of the upper state
           lower_state = state instance of the lower state
        returns:
          string = vibrational label for the transition
        """

        # Get string which identifies the vibrational states involved in the transition
        if upper_state.QuantumNumbers.vibstate == lower_state.QuantumNumbers.vibstate:
            t_state = str(upper_state.QuantumNumbers.vibstate).strip()
        else:
            v_dict = {}
            for label in list(set(upper_state.QuantumNumbers.qn_dict.keys() + lower_state.QuantumNumbers.qn_dict.keys())):
                if specmodel.isVibrationalStateLabel(label):
                    try:
                        value_up = upper_state.QuantumNumbers.qn_dict[label]
                    except:
                        value_up = 0
                    try:
                        value_low = lower_state.QuantumNumbers.qn_dict[label]
                    except:
                        value_low = 0
                    v_dict[label] = [value_up, value_low]
            v_string = ''
            valup_string = ''
            vallow_string = ''
            for v in v_dict:
                v_string += "%s," % v
                valup_string += "%s," % v_dict[v][0]
                vallow_string += "%s," % v_dict[v][1]
            # do not distinct between upper and lower state
            # create just one label for both cases
            if valup_string < vallow_string:
                dummy = vallow_string
                vallow_string = valup_string
                valup_string = dummy
            if len(v_dict) > 1:
                t_state = "(%s)=(%s)-(%s)" % (v_string[:-1], valup_string[:-1], vallow_string[:-1])
            else:
                t_state = "%s=%s-%s" % (v_string[:-1], valup_string[:-1], vallow_string[:-1])

            #t_state = '(%s)-(%s)' % (upper_state.QuantumNumbers.vibstate,lower_state.QuantumNumbers.vibstate)

        return t_state


    ##********************************************************************
    def createatomname(self, atom):
        """
        Creates a name for an atom. The format is
        (massnumber)(elementsymbol)(charge): e.g. 13C+, 12C+
        """

        try:
            charge = int(atom.IonCharge)
        except AttributeError:
            charge = 0

        symbol = atom.ChemicalElementSymbol

        if charge == 0:
            charge_str = ''
        elif charge == 1:
            charge_str = '+'
        elif charge == -1:
            charge_str = '-'
        else:
            charge_str = str(charge)

        try:
            massnumber = atom.MassNumber
        except AttributeError:
            massnumber = ''

        return "%s%s%s" % (massnumber, atom.ChemicalElementSymbol, charge_str)

    
