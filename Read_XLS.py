# ----------------------------------
# Author: Lauren Makely
# Affiliation: Clark Nexsen
# Date: June 15, 2015
# ----------------------------------

import os
import shutil
import arcpy

wrkbk = r""
shp = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\shps\CAD_Polygons_Gaeta_SE.shp"

def backup_shapefile(source_shp):
    """ copies a shapefile and all its metadata """

    metalist = [".cpg", ".dbf", ".prj", ".shp.xml" ,".shx"]
    head, tail = os.path.split(source_shp)

    copylist = [source_shp]
    for metaitem in metalist:
        copylist.append(source_shp.replace(".shp",metaitem))

    # create backupdir
    backupdir = os.path.join(head,"{0}_backup".format(tail.replace(".shp","")))
    if os.path.isdir(backupdir):
        shutil.rmtree(backupdir)
        os.makedirs(backupdir)
    else:
        os.makedirs(backupdir)

    # copy files into the directory
    for copy in copylist:
        shutil.copy(copy, os.path.join(backupdir, os.path.basename(copy)))

    print("Backup created at {0}".format(backupdir))
    return

def read_attributes(shp_filepath):
    """
    Returns a python table of input shapefiles attribute table
    """

    # create a backup of the shapefile
    #backup_shapefile(shp_filepath)
    
    # find the field names
    field_names = []
    fields      = arcpy.ListFields(shp_filepath)
    
    print("Shapefile has the following fields:")
    for field in fields:
        print field.baseName
        field_names.append(field.baseName)

    onlist = ["Layer", "Level", "Color", "LyrColor", "LineWt", "RefName"]
    print "--------------------------------"
    print "Searching for desired fields: "
    print " " + ", ".join(onlist)
    
    with arcpy.da.SearchCursor (fields, onlist) as cursor:
        for row in cursor:
            print "{0}  |{1}    |{2}    |{3}    |{4}    |{5}    |".format(row[0],row[1],row[2],row[3],row[4],row[5])
    
    return

backup_shp =r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb\CAD_Temporary\CAD_Polygons_Gaeta_SE"

read_attributes(backup_shp)

### Pseudo Code below:
##  faillist = []

##  if Level_Name == " "
##        faillist.append(Level_Name)
##  if len(CO) > 1 or len(CO)=0:
##        faillist.append(Level_Name)
