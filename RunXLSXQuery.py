__author__ = 'lmakely'

from xls_class import xls_class
import arcpy
arcpy.env.overwriteOutput = True

def SelectFeatures(input_xls, input_gdb):

    # defines excel document
    xc = xls_class()
    xc.read(input_xls)

    # creates a list of queries to perform on the shapefile
    query_list = xc.worksheets["CAD_SDS"][1:,13]

    for layer in mapLayers:
        desc = arcpy.Describe(layer)
        print "Querying " + desc.name

        i = 1
        for query in query_list:
            try:
                out_name = xc.worksheets["CAD_SDS"][i, 12]
                new_name = input_gdb + "\\" + out_name
                print "Searching feature class: " + out_name
                arcpy.Select_analysis(layer, new_name, query)
                print out_name + " exported"
            except:
                print "Expression returned no results"
            i = i + 1

    return

if __name__ == "__main__":

    working_gdb = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    mxd = arcpy.mapping.MapDocument(r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd")
    mapLayers = arcpy.mapping.ListLayers(mxd)
    xls_file = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Cad_Label_to_SDS.xlsx"
    SelectFeatures(xls_file, working_gdb)