import os, shutil
from dnppy import core 

filelist= core.list_files(False, "V://Projects//5088_MOD_NAVFAC_LANT_Asset_Management//Field//Maps//Scans//SW//NEW STUFF TO PROCESSSSSSSSS", ".pdf", False)

def sort(filelist, delim = "_"):

   for filename in filelist:
       head,tail = os.path.split(filename)

       tail_list = tail.split(delim)

       print "Beginning to move " + tail
       move_dir = os.path.join(head, tail_list[0])

       if not os.path.exists(move_dir):
           os.makedirs(move_dir)

       print tail + " moved to folder"
       shutil.move(filename, os.path.join(move_dir, tail))

   return

print "Sorting files"
sort(filelist,"_")
