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

    # determines the project naming convention
    project = input("Which project number are you working on?")

    # finds all the files in the workspace folder provided
    # if you are only looking for a certain type of file extension,
    # replace the 2nd False with strings (ex: ".shp") or a list of
    # strings (ex: [".shp", ".xml"]
    # The same can be done with the last False to exclude file types
    files = core.list_files(False, filelist, False, False)
    
    for filename in files:
       head,tail = os.path.split(filename)
    
       if project == 5646:
           tail_list = tail[0:4]
           print "Beginning to move " + tail
           move_dir = os.path.join(head, tail_list)

           if not os.path.exists(move_dir):
               os.makedirs(move_dir)

           print tail + " moved to folder"
           shutil.move(filename, os.path.join(move_dir, tail))

       elif project ==  5088:
           delim = "_"
           tail_list = tail.split(delim)
                              
           print "Moving " + tail
           move_dir = os.path.join(head, tail_list[0])

           if not os.path.exists(move_dir):
               os.makedirs(move_dir)

           print tail + " moved to folder"
           shutil.move(filename, os.path.join(move_dir, "_".join(tail_list[1:])))
           print("Moved file '{0}' ".format(filename))
           
    print("Moved all files!")
    return

sort(works)

def NewFileName (recursive, workspace, installation):
    files = core.list_files(recursive, workspace)
    util = os.path.dirname(workspace)
    i = 100

    newname = "{0}-{1}-{2}".format(installation, util,i.zfill(6))
    
    for items in files:
        print items
        original = items[:-4]
        print "Renaming " + original + " to " + newname
        core.rename(items, original, workspace + "\\" + newname)
        i = i +1

# ex: NewFileName(True, works, "13A80")
