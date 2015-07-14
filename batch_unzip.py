__author__ = 'George Kipp'
# Script: batch unzip
# Author: George Kipp
# Created Date: July 10th, 2015
# Last Modified Date: July 11th, 2015
# Description: this script unzips all files in a directory and deletes the zipped files

# Algorithm:
#   get input/output directory
#   loop through directory
#   unzip files
#   delete zipped files

# Modules: arcpy

# Global Variables:
#   input_dir = input directory containing zipped files
#   output_dir =  output directory for unzipped files
#   extension = ".zip"

# Local Variables: none

# Iteration Variables:
#   file_name - full path of file
#   zip_ref - zipfile object

# Input Parameters: input_dir, output_dir

# Output: zip_ref.extractall

# Computation: none

# import modules
import arcpy, os, zipfile

# input_dir = 'E:\\GIS\\LiDAR\\Missouri'
input_dir = arcpy.GetParameterAsText(0)
output_dir = arcpy.GetParameterAsText(1)
extension = ".zip"

os.chdir(input_dir) # change directory from working dir to input_dir with files

try:
    for item in os.listdir(input_dir): # loop through items in input_dir
        if item.endswith(extension): # check for ".zip" extension
            file_name = os.path.abspath(item) # get full path of files
            arcpy.AddMessage("Unzipping {0} to {1}".format(file_name, output_dir))
            zip_ref = zipfile.ZipFile(file_name) # create zipfile object
            zip_ref.extractall(output_dir) # extract file to output_dir
            zip_ref.close() # close file
            os.remove(file_name) # delete zipped file
    arcpy.AddMessage("Extraction complete.")
except:
    arpy.AddError("Error in unzipping files. Please contact support.")
