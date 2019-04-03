# -*- coding: utf-8 -*-

# url where vamdc-database-nodes are registered
#REGURL='http://casx019-zone1.ast.cam.ac.uk/registry/services/RegistryQueryv1_0' # no route to host..
REGURL='http://registry.vamdc.eu/registry-12.07/services/RegistryQueryv1_0' # a node is missing referenceUrl
#REGURL='http://msslkr.phys.ucl.ac.uk/registry-12.07/services/RegistryQueryv1_0' # no route to host..
# sqlite3 database file
#DATABASE_FILE = "cdms_sqlite.db"
DATABASE_FILE = "/var/www/static/cdms/cdms_lite/cdms_lite.db"

#DATABASE_FILE = "/var/www/static/cdms/cdms_lite/cdms_lite_private.db"
# Timeout for queries
TIMEOUT = 100
