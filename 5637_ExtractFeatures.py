__author__ = 'lmakely'

import xls_class from xls_class
import arcpy
import os

def CreateFieldFromXLSX(counter, in_table, feature_class, new_attribute_name, sheet_name):

    # trying to decide if building this in is too much and should be done manually...
    # field will only be created once anyways and could be done by joining features
    # by the RefNames except for lines which need more manipulation

    xc = xls_class()
    xc.read(in_table)

    field_names = []
    fields      = arcpy.ListFields(feature_class)

    # get list of current fields
    for field in fields:
        field_names.append(field.baseName)

    # make description field
    if new_attribute_name not in field_names:
        arcpy.AddField_management(feature_class, new_attribute_name, "TEXT", "","", 255)
        print("Added '{0}' attribute".format(new_attribute_name))

    from_attribute = xc.worksheets[sheet_name][counter, 3]
    print "Calculating attribute as: " + from_attribute
    expression =  '"' + from_attribute + '"'
    arcpy.CalculateField_management(feature_class, new_attribute_name, expression)

    return

def QueryLayer(in_table, sheet_name, input_mxd, input_gdb):

    #sets up map document inputs
    mxd = arcpy.mapping.MapDocument(input_mxd)
    mapLayers = arcpy.mapping.ListLayers(mxd)

    #reads in excel document
    xc = xls_class()
    xc.read(in_table)

    #loops through the line and polygon files for the site
    for layer in mapLayers:
        desc = arcpy.Describe(layer)
        print("Querying {0}".format(desc.name))

            while b < 154:

                #building query formatting
                query = "' " + xc.worksheets[sheet_name][b, 16] + " '"

                # determining inputs for selection type
                ds = xc.worksheets[sheet_name][b, 11]
                fc = xc.worksheets[sheet_name][b, 12]
                i = b - 1
                last_fc = xc.worksheets[sheet_name][i, 12]

                #chooses selection type to
                if fc == last_fc:
                    selection_type = "ADD_TO_SELECTION"
                if fc != last_fc:
                    selection_type = "NEW_SELECTION"

                out_feature_class =  os.path.join(input_gdb, ds , fc)

                arcpy.SelectLayerByAttribute_management (layer, selection_type, query)
                arcpy.CopyFeatures_management (layer, out_feature_class)

    return




if __name__ == "__main__":

    # laurens test area
    gdb = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    gdbdir = "CAD_Temporary"
    mxd = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd"
    xls = r"Reference\Cad_Label_to_SDS.xlsx"
    outdir = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\shps"