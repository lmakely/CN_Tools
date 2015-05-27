from dnppy import core
import os


# Help:
#   !!WARNING!!   Currently this script will rename ALL files in a folder
#                 It will use the first 4 characters to determine the util
#                 Make a backup of files just in case!
#
#   workspace       file path to folder containing items to be renamed
#   installation    Installation code (string)
#   util            The utility code (string) determined by current name

def NewFileName (recursive, workspace, installation):
    files = core.list_files(recursive, workspace)
    i = 100
    head, tail = os.path.split(files[0])
    util = tail[0:4]
    newname = installation + "-" + util + "-000"
    
    for items in files:
        print items
        original = items[:-4]
        new= newname + str(i)
        print "Renaming " + original + " to " + new
        core.rename(items, original, workspace + "\\" + new)
        i = i +1

works = r"C:\LMM\ArcTools\test_folder"

NewFileName(False, works, "13A80")
