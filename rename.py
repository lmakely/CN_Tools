from dnppy import core
import os


# Help:
#     !!WARNING!!   Currently this script will rename ALL files in that folder
#                   I'm working on making it recognized already correct names
#   workspace       file path to folder containing items to be renamed
#   installation    Installation code (string)
#   util            The utility code (string)

def NewFileName (recursive, workspace, installation):
    if os.path.isdir(workspace):
        print "Directory exists, will begin processing files"
    else:
        print "Folder not found. Please check for typos and make sure you have access to the proper drives."

    files = core.list_files(recursive, workspace)
    i = 100
    
    for items in files:
        findFolder = os.path.dirname(items)
        print "Found: " + items
        original = items[:-4]
        head, util = os.path.split(findFolder)

        newname = installation + "-" + util + "-000"
        new= newname + str(i)
        print "Renaming " + original + " to " + new
        core.rename(items, original, workspace + "\\" + new)
        i = i +1

            


works = r"C:\LMM\ArcTools\test folder"
NewFileName(True, works, "13C40")
