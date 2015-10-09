__author__ = 'George Kipp'
# Script: export all coded value domains in a gdb to tables
# Created Date: August 15, 2015
# Last Modified Date: August 15, 2015
# Description:
    # script based on script by matt wilkie
    # (http://gis.stackexchange.com/questions/26215/export-all-coded-value-domains-from-a-geodatabase)

# import modules
import arcpy, os

arcpy.env.workspace = arcpy.GetParameterAsText(0)
gdb = arcpy.env.workspace
arcpy.env.overwriteOutput = True

domains = arcpy.da.ListDomains(gdb)

for domain in domains:
     if domain.domainType == 'CodedValue':
         domain_name = domain.name
         print 'Exporting {0} coded values to table in {1}'.format(domain_name, gdb)
         coded_value_list = domain.codedValues
         print "The coded values / descriptions are"
         for value, descrip in coded_value_list.iteritems():
             print "{0} : {1}".format(value, descrip)
         out_table_name = domain_name.lower()
         arcpy.DomainToTable_management(gdb, domain_name, out_table_name, "item", "descrip")
     else:
         print "{0} not a coded value domain. Passing it up.".format(domain.name)
