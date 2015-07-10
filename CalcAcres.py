__author__ = 'George Kipp'
# Script: calculate acres of an input polygon
# Author: George Kipp
# Created Date: July 8th, 2015
# Last Modified Date: July 10th, 2015
# Description: this script calculates the acreage on an input polygon.

# Algorithm:
#   add field to input polygon
#   use !shape.area@acres! expression to calculate acreage

# Modules: arcpy

# Global Variables: 
#   input_poly = input polygon

# Local Variables: none

# Iteration Variables: none

# Input Parameters: input_poly

# Output: CALC_AC

# Computation: acres

# import modules
import arcpy

arcpy.env.overwriteOutput = True

input_poly = arcpy.GetParameterAsText(0)

# add acres field to dissolved feature class; calculate acreage; use acreage to determine length of smoke
try:
    arcpy.AddField_management(input_poly, "CALC_AC", "Float",)
    expression = "float(!shape.area@acres!)" # expression used for calculating acres
    arcpy.CalculateField_management(input_poly, "CALC_AC", expression, "PYTHON")
except:
    arcpy.AddError("Error calculating acres. Please contact support.")
