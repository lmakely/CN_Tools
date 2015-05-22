import os, shutil

from dnppy import core

def sort(filelist, delim = "_"):

    for filename in filelist:
        head,tail = os.path.split(filename)

        tail_list = tail.split(delim)
        move_dir = os.path.join(head, tail_list[0])

        if not os.path.exists(move_dir):
            os.makedirs(move_dir)

        shutil.move(filename, os.path.join(move_dir, "_".join(tail_list[1:])))
        print("Moved file '{0}' ".format(filename))

    print("Moved all files!")
    return



if __name__ == "__main__":
    
    filelist = core.list_files(False, r"C:\Users\jwely\Desktop\troubleshooting\lauren_organize")
    sort(filelist)
    
    
        
