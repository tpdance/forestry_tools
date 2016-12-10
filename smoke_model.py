__author__ = 'George Kipp'
# Script: prescribed fire smoke model
# Author: George Kipp
# Created Date: March 27th, 2015
# Last Modified Date: May 25th, 2015
# Description: This script creates a polygon that models the likely dispersion path of smoke from a
#   prescribed fire operation. The script takes an input polygon, dissolves (it if it's a singlepart
#   feature), adds an acreage field, then creates bearing lines at +/- 30 degrees of the wind
#   direction. Finally, this script converts the separate bearing lines to a polygon.

# Modules: arcpy, os

# Global Variables:
#   input_fc
#   output_fc
#   wind_from
#   coord_sys
#   wind_to
#   wind_plus
#   wind_minus

# Local Variables: none

# Iteration Variables: row, feature, pt, item, coord, pair

# Input Parameters: input_fc, wind_from, output_fc, coordsys

# Output: smoke_model

# Computation: wind_plus, wind_minus

# import modules
import arcpy, os

# okay to overwrite output
arcpy.env.overwriteOutput = True

# initialize globals
input_fc = arcpy.GetParameterAsText(0) # input feature class
wind_from = arcpy.GetParameterAsText(1) # wind direction
output_fc = arcpy.GetParameterAsText(2) # output feature class
coord_sys = arcpy.GetParameterAsText(3) # coordinate system
out_space = os.path.dirname(output_fc) # output workspace
if os.path.dirname(output_fc).endswith(".gdb"):
    arcpy.AddMessage("The output feature class is located in a geodatabase")
else:
    arcpy.AddMessage("The output feature class is a shapefile")

# checks if output feature class is a geodatabase and add appropriate file extension
def gdb_check():
    suffix = os.path.dirname(output_fc)
    if suffix.endswith(".gdb") or suffix.endswith(".mdb"):
        extension = ""
    else:
        extension = ".shp"
    return extension

# checks if output attribute table is a geodatabase and adds appropriate file extension
def table_check():
    table_suffix = os.path.dirname(output_fc)
    if table_suffix.endswith(".gdb") or table_suffix.endswith(".mdb"):
        ext = ""
    else:
        ext = ".dbf"
    return ext

# deal with wind direction greater than 360
# calculate wind_to, wind_plus, and wind_minus
wind_from = float(wind_from)
wind_from = (wind_from - 360)%360
wind_to = (wind_from-180)%360
arcpy.AddMessage("The wind is coming from {0} and blowing to {1}.".format(wind_from, wind_to))
wind_plus = (wind_to + 30)%360
wind_minus = (wind_to - 30)%360
arcpy.AddMessage("The wind spread is {0} to {1}.".format(wind_plus, wind_minus))

# dissolve singlepart polygons to multipart
try:
    dissolve_name = out_space + r"\burn_dissolve" + gdb_check()
    dissolve_poly = arcpy.Dissolve_management(input_fc, dissolve_name, "", "", "MULTI_PART", "")
    arcpy.AddMessage("Successfully dissolved polygon.")
except:
    arcpy.AddError("Error dissolving polygon.")

# add acres field to dissolved feature class; calculate acreage; use acreage to determine length of smoke
try:
    arcpy.AddField_management(dissolve_poly, "GIS_AC", "Float",)
    expression = "float(!shape.area@acres!)" # expression used for calculating acres
    arcpy.CalculateField_management(dissolve_poly, "GIS_AC", expression, "PYTHON")
    #smoke_distance_list = [] # uses list to deal with singlepart polygons (relic if i want to deal with singlepart polygons)
    with arcpy.da.SearchCursor(dissolve_poly, "GIS_AC") as srCursor:
        for row in srCursor:
            if row[0] > 250:
                dist = 10
            else:
                dist = 5
            #smoke_distance_list.append(dist) # relic if i want to deal with singlepart polygons
    smoke_distance = dist
    arcpy.AddMessage("Successfully calculated acreage. The burn is {0} acres, with a smoke trajectory of {1} miles.".format(row[0], dist))
except:
    arcpy.AddError("Error calculating acreage.")

# create centroid point feature class of burn polygon
try:
    centroid_name = "centroid" + gdb_check()
    centroid_point = arcpy.CreateFeatureclass_management(out_space, centroid_name, "POINT", "", "DISABLED", "DISABLED", coord_sys)
    arcpy.AddField_management(centroid_point, "X", "FLOAT",) # X coordinate of centroid point
    arcpy.AddField_management(centroid_point, "Y", "FLOAT",) # Y coordinate of centroid point
    arcpy.AddField_management(centroid_point, "DIST", "FLOAT") # distance for smoke line
    arcpy.AddField_management(centroid_point, "BR_PLUS", "FLOAT") # wind_plus bearing
    arcpy.AddField_management(centroid_point, "BR_MINUS", "FLOAT") # wind_minus bearing

    # use search cursor to find centroid of input feature class
    cursor = arcpy.da.SearchCursor(dissolve_poly, "SHAPE@XY")
    centroid_coord = []

    # check if centroid point is in a geodatabase and, if not, add .shp extension
    centroid_name_path = os.path.join(os.path.dirname(out_space), os.path.basename(out_space)) + r"\centroid" + gdb_check()
    centroid_name_check = os.path.dirname(centroid_name_path)

    # check if centroid point is in a geodatabase and assigns field names appropriately
    if centroid_name_check.endswith("gdb") or centroid_name_check.endswith(".mdb"):
        centroid_field_list = ["ObjectID", "X", "Y", "DIST", "BR_PLUS", "BR_MINUS", "SHAPE@"]
    else:
        centroid_field_list = ["ID", "X", "Y", "DIST", "BR_PLUS", "BR_MINUS", "SHAPE@"]

    for feature in cursor:
        centroid_coord.append(feature[0])
    point = arcpy.Point()
    for pt in centroid_coord:
        point.X = float(pt[0])
        #print pt[0]
        point.Y = float(pt[1])
        #print pt[1]
        pid = 1
        distance = smoke_distance
        # use insert cursor to insert centroid coordinates into centroid point
        with arcpy.da.InsertCursor(centroid_point, centroid_field_list) as isCursor:
            for item in pt:
                XCoord = float(pt[0])
                YCoord = float(pt[1])
                new_point = [pid, pt[0], pt[1], distance, wind_plus, wind_minus, arcpy.Point(XCoord, YCoord)]
                isCursor.insertRow(new_point)
    del cursor
    arcpy.AddMessage("Successfully created centroid point")
except:
    arcpy.AddError("Error creating centroid point.")

# use centroid feature as input for bearing/distance to line
# create lines from centroid points, wind_plus, and wind_minus
try:
    in_table = out_space + r"\centroid" + table_check()
    line_plus_fc = out_space + r"\smoke_lines_plus" + gdb_check()# output feature class name
    line_minus_fc = out_space + r"\smoke_lines_minus" + gdb_check()
    merge_lines = out_space + r"\merge_lines" + gdb_check()
    arcpy.BearingDistanceToLine_management(in_table, line_plus_fc, "X", "Y", "DIST", "MILES", "BR_PLUS", "DEGREES")
    arcpy.BearingDistanceToLine_management(in_table, line_minus_fc, "X", "Y", "DIST", "MILES", "BR_MINUS", "DEGREES")

    # merge separate lines and dissolve them into multipart feature class
    arcpy.Merge_management([line_plus_fc, line_minus_fc], merge_lines) # merge line_plus and line_minus
    smoke_lines = out_space + r"\smoke_lines" + gdb_check()
    arcpy.Dissolve_management(merge_lines, smoke_lines, "", "", "MULTI_PART", "")

    # delete intermediate data
    arcpy.Delete_management(line_plus_fc) # delete intermediate data
    arcpy.Delete_management(line_minus_fc) # delete intermediate data
    arcpy.Delete_management(merge_lines) # delete intermediate data
    arcpy.AddMessage("Successfully created and merged bearing lines.")
except:
    arcpy.AddError("Error creating bearing lines.")

# use update cursor to get vertex coordinates of smoke lines
try:
    desc = arcpy.Describe(smoke_lines)
    shape_field_name = desc.ShapeFieldName
    test_for_coords = arcpy.UpdateCursor(smoke_lines)
    poly_array = arcpy.Array()
    for coord in test_for_coords:
        sample = coord.getValue(shape_field_name)
        for item in sample:
            for pair in item:
                #print pair.X, pair.Y
                poly_array.add(arcpy.Point(pair.X, pair.Y))
    del test_for_coords

    # create smoke model feature class
    smoke_name = os.path.basename(output_fc)
    smoke_model = arcpy.CreateFeatureclass_management(out_space, smoke_name, "POLYGON", "", "DISABLED", "DISABLED", coord_sys)

    # check if smoke model is in a geodatabase and assign appropriate fields
    smoke_model_path = os.path.join(os.path.dirname(out_space), os.path.basename(out_space)) + output_fc + gdb_check()
    smoke_ext_check = os.path.dirname(smoke_model_path)
    if smoke_ext_check.endswith(".gdb") or smoke_name.endswith(".mdb"):
        smoke_fields = ["ObjectID", "SHAPE@"]
    else:
        smoke_fields = ["ID", "SHAPE@"]

    # use array and insert cursor to create polygon from lines
    line_id = 1
    with arcpy.da.InsertCursor(smoke_model, smoke_fields) as insCursor:
        insCursor.insertRow([line_id, arcpy.Polygon(poly_array)])

    # delete intermediate data
    arcpy.Delete_management(centroid_point)
    arcpy.Delete_management(smoke_lines)
    arcpy.Delete_management(dissolve_poly)
    arcpy.AddMessage("Successfully created smoke model. Regards: " + __author__)
    arcpy.AddMessage("Even better than a machine that goes, PING!")
except:
    arcpy.AddError("Error creating smoke model. Please contact " + __author__ + " for help.")
