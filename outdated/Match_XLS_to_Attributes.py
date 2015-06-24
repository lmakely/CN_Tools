# ----------------------------------
# Author: Lauren Makely
# Affiliation: Clark Nexsen
# Date: June 15, 2015
# ----------------------------------

import arcpy
import os
from xls_class import xls_class as xc


def LnTypeToLC(Linetype):
    if Linetype   == "Continuous":
        return 0
    elif Linetype == "Dotted":
        return 1
    elif Linetype == "Dashed":
        return 2
    elif Linetype == "Dashedspaced":
        return 3
    elif Linetype == "Dasheddotted":
        return 4
    elif Linetype == "Dasheddouble-dotted":
        return 6
    elif Linetype == "Chain":
        return 7


def NewAttributeFromFunction(shapefilepath, new_attribute_name, function, function_arg_att_names):
    """
    Creates a new attribute with values according to an input function

    :param shapefilepath:
    :param new_attribute_name:      name for new field to create
    :param function:                function object for function by which to determine new values for new attribute
    :param function_arg_att_names   attribute names to use as function arguments, must be a list.
    :return:
    """

    # get list of current fields
    field_names = arcpy.ListFields(shapefilepath)

    # make sure list of "from_attribute" are all valid fields
    for att in function_arg_att_names:
        if att not in field_names:
            raise ValueError("This shapefile has no fields named {0}".format(att))


    if new_attribute_name not in field_names:
        arcpy.AddField_management(shapefilepath, new_attribute_name, field_type = "short")
        print("Attribute '{0} created".format(new_attribute_name))
        print("Calculating values for each entry from other attributes")

        rows = arcpy.UpdateCursor(shapefilepath)
        for row in rows:
            args      = [getattr(row, att) for att in function_arg_att_names]
            new_value = function(*args)
            setattr(row, new_attribute_name, new_value)
            rows.updateRow(row)

    else:
        raise ValueError("This shapefile already has a field named '{0}'".format(new_attribute_name))

    return



def NewAttributeByConcatenation(shapefilepath, new_attribute_name, from_attributes):
    """
    Creates a new attribute and value by concatenating the values of existing attributes

    :param shapefilepath:           filepath to shapefile
    :param new_attribute_name:      name of new attribute to be created in a new field
    :param from_attributes:         list of attributes from which to create the new attributes value

    :return
    """

    # get list of current fields
    field_names = arcpy.ListFields(shapefilepath)

    # make sure list of "from_attribute" are all valid fields
    for from_attribute in from_attributes:
        if from_attribute not in field_names:
            raise ValueError("This shapefile has no fields named {0}".format(from_attribute))

    if new_attribute_name not in field_names:
        arcpy.AddField_management(shp_filepath, new_attribute_name, field_type = "short")
        print("Added '{0}' attribute".format(new_attribute_name))

        rows = arcpy.UpdateCursor(shapefilepath)
        for row in rows:
            # get list of attributes
            attributes = [getattr(row, att) for att in from_attributes]
            new_value  = "_".join(map(str, attributes))
            setattr(row, new_attribute_name, new_value)

    else:
        raise ValueError("This shapefile already has a field named '{0}'".format(new_attribute_name))

    return

def SelectFeatureClass():

    return


def ExportShape():

    return

    # join Matching_XL
    #arcpy.JoinField_management (shp_filepath, "MatchField", in_list, "MatchingField", ["Feature_Class"])

    # select by attribute the feature_classes that are the same

##    with arcpy.da.SearchCursor (shp_filepath, "MatchField") as cursor:
##        for row in cursor:
##            whereClause = "MatchField = "
##            arcpy.SelectLayerByAttribute_management(Shapes, "NEW_SELECTION", whereClause)



# woo stuff
if __name__ == "__main__":

    # testing match attributes
    geodb_filepath  = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    shp_filepath    = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb\CAD_Temporary\CAD_Polygons_Gaeta_SE"
    in_list_path    = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Matching_XL.xlsx"

    # ID fields in shapefile
    fields      = arcpy.ListFields(shp_filepath)
    print("Shapefile has the following fields:")
    print(fields)
    print("-"*30)

    # defines xlsx
    #onsheet = xc()
    #onsheet.read(in_list_xlspath)

    print "Importing feature class table to database"
    # adds xlsx to gdb to temporarily join it to shp
    arcpy.TableToTable_conversion(in_list_path, geodb_filepath, "MatchingXL")
    print "Table added to " + os.path.dirname(geodb_filepath)

    # make LC code field
    NewAttributeFromFunction(shp_filepath, "LC_Code", LnTypeToLC, ["Linecode"])

    # make MatchField field
    table = geodb_filepath + "\MatchingXL"
    from_attributes = arcpy.ListFields(table)[2:8]
    NewAttributeByConcatenation(shp_filepath, "MatchField", from_attributes)

