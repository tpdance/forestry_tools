__author__ = 'George Kipp'
# Script: unzip gzipped data
# Author: George Kipp
# Created Date: July 10th, 2015
# Last Modified Date: July 10th, 2015
# Description: this script unzips files compressed in the GNU gzip format (.tar.gz). this is common for large datasets
#   especially satellite imagery.

# Algorithm:

# Modules: arcpy, gzip, os, shutil

# Global Variables:
# in_path = input directory
# out_path = output directory

# Local Variables: none

# Iteration Variables: item

# Input Parameters: in_path

# Output: outF

# Computation: none

# import modules
import arcpy, gzip, os, shutil

arcpy.env.overwriteOutput = True

# set directory paths
in_path = arcpy.GetParameterAsText(0)
out_path = arcpy.GetParameterAsText(1)

for item in os.listdir(in_path):
    print "Unzipping: " + item
    inF = gzip.open(os.path.join(in_path, item), 'r')
    outF = open(os.path.join(out_path, item[:-3]), 'wb')
    shutil.copyfileobj(inF, outF)
    inF.close()
    outF.close()
