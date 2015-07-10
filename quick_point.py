__author__ = 'George Kipp'
# Script: quick create point
# Author: George Kipp
# Created Date: June 19th, 2015
# Last Modified Date: June 19th, 2015
# Description: allows user to quickly create a point feature class with only name, output workspace, and coordinate
# as input.

# Algorithm:

# Modules: arcpy

# Global Variables:
# out_name - name of output point
# out_workspace - name of output workspace
# coord_sys - coordinate system
# point_name - out name concatenated with appropriate extension
# new_point - new point feature class

# Local Variables: none

# Iteration Variables: none

# Input Parameters: out_name, out_workspace, coord_sys

# Output: new_point

# Computation: gdb_check

# import modules
import arcpy

arcpy.env.overwriteOutput = True

out_name = arcpy.GetParameterAsText(0)
out_workspace = arcpy.GetParameterAsText(1)
coord_sys = arcpy.GetParameterAsText(2)
# coord_sys = arcpy.SpatialReference(26915) - NAD83, UTM Zone 15N

file_ext = out_workspace[-4:]

if file_ext == ".gdb" or file_ext == ".mdb":
    arcpy.AddMessage("The output feature class is located in a geodatabase.")
else:
    arcpy.AddMessage("The output feature class is a shapefile.")

def gdb_check():
    if file_ext == ".gdb" or file_ext == ".mdb":
        extension = ""
    else:
        extension = ".shp"
    return extension

try:
    point_name = out_name + gdb_check()
    new_point = arcpy.CreateFeatureclass_management(out_workspace, point_name, "POINT", "", "DISABLED", "DISABLED", coord_sys)
    arcpy.AddMessage("Successfully created point.")
except:
    arcpy.AddError("Operation failed. Please contact support.")
