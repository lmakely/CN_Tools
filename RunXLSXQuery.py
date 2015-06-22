__author__ = 'lmakely'

from xls_class import xls_class
import arcpy
arcpy.env.overwriteOutput = True

def SelectFeatures(input_xls, input_gdb):

    # defines excel document and creates empty list for queries
    xc = xls_class()
    xc.read(input_xls)

    # creates a list of queries to perform on the shapefile
    query_list = xc.worksheets["CAD_SDS"][1:,13]

    for query in query_list:
        print query
    return


def ExportSelection():

    return

if __name__ == "__main__":


    working_gdb = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    mxd = arcpy.mapping.MapDocument(r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace")
    mapLayers = arcpy.mapping.ListLayers(mxd)
    xls_file = r"Reference\Cad_Label_to_SDS.xlsx"

    SelectFeatures(xls_file, working_gdb)
    ExportSelection()