import tkinter as tk
import os
from tkFileDialog import askopenfilename
import tkMessageBox

__author__ = 'George Kipp'
# date created: 7/27/17
# last modified: 7/27/17
# abstract: this script is used to convert csv files from MOForest into .dbi files so that they can be imported into MOFITS

done = False

while not done:
    # open file browser to navigate to .dbi file
    root = tk.Tk()
    root.withdraw()

    file_path = askopenfilename(parent=root)

    dirname = os.path.dirname(file_path)
    file_name = os.path.splitext(os.path.basename(file_path))[0]
    ext = os.path.splitext(os.path.basename(file_path))[1]
    # print for error checking
    # print "the dirname is: {0}, the file name is: {1}, and the ext is {2}".format(dirname, file_name, ext)

    # check to see if input file is a csv
    if ext == '.csv':
            infile = os.path.abspath(file_path)
            outfile = str(os.path.join(dirname, file_name)) + ".dbi"
            with open(infile, 'rb') as reader, open(outfile, 'wb') as writer:
                for line in reader:
                    newline = line.strip('\r\n') + ',,,'
                    writer.write(newline)
                    writer.write('\r\n')
                done = True
    # exception handling, if wrong file type, throw error message
    else:
        done = False
        tkMessageBox.showinfo("DANGER", "Incorrect input file. Please try again")
        print "File is the incorrect format, please try again."
