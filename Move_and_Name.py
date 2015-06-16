# Author: Lauren Makely (CN) and Jeff Ely (NASA DEVELOP)
# Created: May 22, 2015
# Last Update: May 27, 2015

import os, shutil
from dnppy import core 

works = r"C:\LMM\ArcTools\test_folder"

def sort(filelist):
    # moves files to a folder named after them
    # must decide which part of the filename you want
    # Script will ask you for a project number in order to format the
    #   the name of the folder correctly
    # If another project has a specific naming convention you would like to add just let me know!

    # determines the project naming convention
    project = input("Which project number are you working on?")

    # finds all the files in the workspace folder provided
    # if you are only looking for a certain type of file extension,
    # replace the 2nd False with strings (ex: ".shp") or a list of
    # strings (ex: [".shp", ".xml"]
    # The same can be done with the last False to exclude file types
    files = core.list_files(False, filelist, False, False)
    
    for filename in files:
       head,tail = os.path.split(filename) #identifies the name of the file
    
       if project == 5646:
           tail_list = tail[0:4] #finds the utility type
           print "Beginning to move " + tail #moves to corresponding folder
           move_dir = os.path.join(head, tail_list)

           if not os.path.exists(move_dir):
               os.makedirs(move_dir) # if the folder doesn't already exist in workspace, its now created

           print tail + " moved to folder"
           shutil.move(filename, os.path.join(move_dir, tail))

       elif project ==  5088:
           delim = "_"
           tail_list = tail.split(delim) #finds the utility type
                              
           print "Moving " + tail #moves to corresponding folder
           move_dir = os.path.join(head, tail_list[0])

           if not os.path.exists(move_dir):
               os.makedirs(move_dir)  # if the folder doesn't already exist in workspace, its now created

           shutil.move(filename, os.path.join(move_dir, "_".join(tail_list[1:])))
           print("Moved file '{0}' ".format(filename))
           
    print("Moved all files!")
    return
works = r"C:\LMM\5646\test"
sort(works)

def NewFileName (recursive, workspace, installation):
    #finds files to name
    files = core.list_files(recursive, workspace)
    i = 100
        
    for items in files:
        head, util = os.path.split(os.path.dirname(items))
        
        print items
        original = items[:-4]
        newname = "{0}-{1}-{2}".format(installation, util, "000"+str(i))
        print "Renaming " + original + " to " + newname
        core.rename(items, original, workspace + "\\" + newname)
        i = i +1


NewFileName(True, works, "13C70")
