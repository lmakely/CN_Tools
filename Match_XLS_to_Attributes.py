# ----------------------------------
# Author: Lauren Makely
# Affiliation: Clark Nexsen
# Date: June 15, 2015
# ----------------------------------

import os
import shutil
import arcpy
from xls_class import xls_class as xc
from pprint import pprint
import read_att_table

wrkbk1 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Matching_XL.xlsx"
wrkbk2 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\fields_on.xlsx"
shp = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\shps\CAD_Polygons_Gaeta_SE.shp"

def read_attributes(shp_filepath, in_list):
    """
    Returns a python table of input shapefiles attribute table
    """

    # find the field names
    field_names = []
    faillist = []
    fields      = arcpy.ListFields(shp_filepath)

    # ID fields in shpaefile
    print("Shapefile has the following fields:")
    for field in fields:
        print field.baseName
        field_names.append(field.baseName)
        
    print "--------------------------------"

    # defines xlsx
    onsheet = xc()
    onsheet.read(in_list)

    # read xlsx to print headers to be joined
    print "Searching for desired fields: "
    wanted = onsheet.worksheets["CAD_SDS"][0,2:8]
    print " " + ", ".join(wanted)

    print "--------------------------------"

    expression = "[" + "]&[".join(wanted) + "]"
    print "Joining together " + expression
    # make new field for query
    if "MatchField" not in field_names:
        arcpy.AddField_management(shp_filepath, "MatchField", field_type = "text")
    # creates query statement
    arcpy.CalculateField_management (shp_filepath, "MatchField", expression)
    
##    with arcpy.da.SearchCursor (shp_filepath, "MatchField") as cursor:
##        for row in cursor:
##            print row
    return


#read_att_table.backup_shapefile(shp)
backup_shp =r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb\CAD_Temporary\CAD_Polygons_Gaeta_SE"

read_attributes(backup_shp, wrkbk1)

### Pseudo Code below:
##  if Level_Name == " "
##        faillist.append(Level_Name)
##  if len(CO) > 1 or len(CO)=0:
##        faillist.append(Level_Name)



