import os, shutil
from dnppy import core 

works = r"C:\LMM\ArcTools\test folder\uptp"

def sort(filelist):
    files = core.list_files(False, filelist, False, False)
    for filename in files:
       head,tail = os.path.split(filename)

       tail_list = tail[6:10]

       print "Beginning to move " + tail
       move_dir = os.path.join(head, tail_list)

       if not os.path.exists(move_dir):
           os.makedirs(move_dir)

       print tail + " moved to folder"
       shutil.move(filename, os.path.join(move_dir, tail))

    return

##print "Sorting files"
##sort(works)

def NewFileName (recursive, workspace, installation, util):
    files = core.list_files(recursive, workspace)
    print files
    i = 100
    newname = installation + "-" + util + "-000"
    
    for items in files:
        print items
        original = items[:-4]
        new= newname + str(i)
        print "Renaming " + original + " to " + new
        core.rename(items, original, workspace + "\\" + new)
        i = i +1


NewFileName(False,works, "13C40", "uptp")
