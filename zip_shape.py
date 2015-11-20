#**********************************************************************
# Description:
#    Zips the contents of a folder.
# Parameters:
#   0 - Input folder.
#   1 - Output zip file. It is assumed that the user added the .zip 
#       extension.  
#**********************************************************************

# Import modules and create the geoprocessor
#
import sys, zipfile, arcpy, os, traceback

# Function for zipping files.  If keep is true, the folder, along with 
#  all its contents, will be written to the zip file.  If false, only 
#  the contents of the input folder will be written to the zip file - 
#  the input folder name will not appear in the zip file.
#
def zipws(path, zip, keep):
    path = os.path.normpath(path)
    # os.walk visits every subdirectory, returning a 3-tuple
    #  of directory name, subdirectories in it, and file names
    #  in it.
    #
    for (dirpath, dirnames, filenames) in os.walk(path):
        # Iterate over every file name
        #
        for file in filenames:
            # Ignore .lock files
            #
            if not file.endswith('.lock'):
                arcpy.AddMessage("Adding %s..." % os.path.join(path, dirpath, file))
                try:
                    if keep:
                        zip.write(os.path.join(dirpath, file),
                        os.path.join(os.path.basename(path), os.path.join(dirpath, file)[len(path)+len(os.sep):]))
                    else:
                        zip.write(os.path.join(dirpath, file),            
                        os.path.join(dirpath[len(path):], file)) 
                        
                except Exception, e:
                    arcpy.AddWarning("    Error adding %s: %s" % (file, e))

    return None

if __name__ == '__main__':
    try:
        # Get the tool parameter values
        #
        infolder = arcpy.GetParameterAsText(0)
        outfile = arcpy.GetParameterAsText(1)      
        
        # Create the zip file for writing compressed data. In some rare
        #  instances, the ZIP_DEFLATED constant may be unavailable and
        #  the ZIP_STORED constant is used instead.  When ZIP_STORED is
        #  used, the zip file does not contain compressed data, resulting
        #  in large zip files. 
        #
        try:
                zip = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_DEFLATED)
                zipws(infolder, zip, True)
                zip.close()
        except RuntimeError:
                # Delete zip file if it exists
                #
                if os.path.exists(outfile):
                        os.unlink(outfile)
                zip = zipfile.ZipFile(outfile, 'w', zipfile.ZIP_STORED)
                zipws(infolder, zip, True)
                zip.close()
                arcpy.AddWarning("    Unable to compress zip file contents.")
                   
        arcpy.AddMessage("Zip file created successfully")

    except:
        # Return any Python specific errors as well as any errors from the geoprocessor
        #
        tb = sys.exc_info()[2]
        tbinfo = traceback.format_tb(tb)[0]
        pymsg = "PYTHON ERRORS:\nTraceback Info:\n" + tbinfo + "\nError Info:\n    " + \
                str(sys.exc_type)+ ": " + str(sys.exc_value) + "\n"
        arcpy.AddError(pymsg)

        msgs = "GP ERRORS:\n" + arcpy.GetMessages(2) + "\n"
        arcpy.AddError(msgs)
