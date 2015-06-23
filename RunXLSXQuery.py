__author__ = 'lmakely'

from xls_class import xls_class
import arcpy
arcpy.env.overwriteOutput = True

def SelectFeatures(input_xls, input_gdb, mapLayers):

    # defines excel document
    xc = xls_class()
    xc.read(input_xls)
    query_list = []

    # creates a list of queries to perform on the shapefile

    print("Running query list on all layers")
    for layer in mapLayers:
        desc = arcpy.Describe(layer)
        print("Querying {0}".format(desc.name))
        b = 1
        while b < 240:
            ln = xc.worksheets["CAD_SDS"][b,4]
            lv = xc.worksheets["CAD_SDS"][b,5]
            co = xc.worksheets["CAD_SDS"][b,6]
            lt = xc.worksheets["CAD_SDS"][b,7]
            lw = xc.worksheets["CAD_SDS"][b,9]
            ref = xc.worksheets["CAD_SDS"][b,0]

            q1 = '"LEVEL_NAME" = '
            q2 = ' AND "LEVEL" = '
            q3 = ' AND "COLOR" = '
            q4 = ' AND "LINETYPE" = '
            q5 = ' AND "LINEWT" = '
            q6 = ' AND "REFNAME" = '

            test_query = "'{0}' '{1}' '{2}' '{3}' '{4}' '{5}' '{6}' '{7}' '{8}' '{9}' '{10}' '{11}' '{12}'".format(q1,ln,q2,int(lv),q3,int(co),q4,lt,q5,int(lw),q6,ref)
            query = """ %s """ %test_query
            try:
                out_name = xc.worksheets["CAD_SDS"][b, 12]
                
                print("Searching feature class: " + out_name)
                print("inputs are: ")
                print desc.name + ", " + out_name+ ", " + query

                tempPoly = arcpy.CreateFeatureclass_management(input_gdb, "tempPolys", "POLYGON")
                arcpy.Select_analysis(layer, tempPoly, query)
                tempPoly = arcpy.FeatureToPolygon_management(tempPoly, out_name)
                arcpy.Delete_management(tempPoly)
                print out_name + " exported"

            except:
                print "     Expression returned no results"
                
            b = b + 1

    return


if __name__ == "__main__":

    working_gdb = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    mxd = arcpy.mapping.MapDocument(r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd")
    mapLayers = arcpy.mapping.ListLayers(mxd)
    xls_file = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Cad_Label_to_SDS.xlsx"
    SelectFeatures(xls_file, working_gdb, mapLayers)