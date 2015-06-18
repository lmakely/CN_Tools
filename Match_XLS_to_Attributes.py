# ----------------------------------
# Author: Lauren Makely
# Affiliation: Clark Nexsen
# Date: June 15, 2015
# ----------------------------------

import os
import shutil
import arcpy
from xls_class import xls_class as xc
import read_att_table

wrkbk1 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Matching_XL.xlsx"
wrkbk2 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\fields_on.xlsx"
shp = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\shps\CAD_Polygons_Gaeta_SE.shp"
##mxd = arcpy.mapping.MapDocument("V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd")


def Match_attributes(geodb, shp_filepath, in_list):
    """
    Returns a python table of input shapefiles attribute table
    """

    # find the field names
    field_names = []
    faillist = []
    fields      = arcpy.ListFields(shp_filepath)

##    # sets up mxd parameters
##    df = arcpy.mapping.ListDataFrames(mxd, "Layers") [0]
##    Shapes = arcpy.mapping.ListLayers(mxd, "CAD_Polygons_Gaeta_SE", df)[0]

    # ID fields in shapefile
    print("Shapefile has the following fields:")
    for field in fields:
        print field.baseName
        field_names.append(field.baseName)
        
    print "--------------------------------"

    # defines xlsx
    onsheet = xc()
    onsheet.read(in_list)

    # would it be easier to import this as a table at this point and read that?
    TableToTable_conversion (in_list, geodb, "MatchingXL")
    # read xlsx to print headers to be joined
    print "Searching for desired fields: "

    # with xlrd
    #wanted = onsheet.worksheets["CAD_SDS"][0,2:8]
    #print " " + ", ".join(wanted)

    # with arcpy
    table = gdb + "\MatchingXL"
    wanted = arcpy.ListFields(table)
    wanted_names = []
    for field in wanted:
        wanted_names.append(field.baseName)
        
    print "--------------------------------"

    # make new fields for querying
    if "LC_Code" not in field_names:
        arcpy.AddField_management(shp_filepath, "LC_Code", field_type = "short")
        print "LC_Code attribute created"
        print "Calculating LC_Code"
        # add code here to convert microstation types to values once field is created
        # and a progress bar of some kind
    ##      Codeblock:
    ##        if Linetype = "Continuous":
    ##            return 0
    ##        elif Linetype = "Dotted":
    ##            return 1
    ##        elif Linetype = "Dashed":
    ##            return 2
    ##        elif Linetype = "Dashed spaced":
    ##            return 3
    ##        elif Linetype = "Dashed dotted":
    ##            return 4
    ##        elif Linetype = "Dashed double-dotted":
    ##            return 6
    ##        elif Linetype = "Chain":
    ##            return 7
    ##    arcpy.CalculateField_management (shp_filepath, "LC_Code", codeblock)

    if "MatchField" not in field_names:
        arcpy.AddField_management(shp_filepath, "MatchField", field_type = "text")
        print "MatchField attribute created"
    elif:      # creates feature query statement as a field
        expression = "[" + "]&[".join(wanted_names) + "]"
        print "Joining together " + expression
        arcpy.CalculateField_management (shp_filepath, "MatchField", expression)
        print "MatchField attribute calculated"

    print "--------------------------------"

    # join Matching_XL
    #arcpy.JoinField_management (shp_filepath, "MatchField", in_list, "MatchingField", ["Feature_Class"])

    # select by attribute the feature_classes that are the same

##    with arcpy.da.SearchCursor (shp_filepath, "MatchField") as cursor:
##        for row in cursor:
##            whereClause = "MatchField = "
##            arcpy.SelectLayerByAttribute_management(Shapes, "NEW_SELECTION", whereClause)

    return


#read_att_table.backup_shapefile(shp)
backup_shp =r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb\CAD_Temporary\CAD_Polygons_Gaeta_SE"
gdb = 

Match_attributes(backup_shp, wrkbk1)



