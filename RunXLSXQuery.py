__author__ = 'lmakely'

from xls_class import xls_class
import arcpy
import os
arcpy.env.overwriteOutput = True

def CreateFieldFromXLSX(feature_class, new_attribute_name):

    field_names = []
    fields      = arcpy.ListFields(feature_class)

    # get list of current fields
    for field in fields:
        field_names.append(field.baseName)

    # make description field
    if new_attribute_name not in field_names:
        arcpy.AddField_management(feature_class, new_attribute_name, field_type = "text")
        print("Added '{0}' attribute".format(new_attribute_name))

    from_attribute = xc.worksheets["CAD_SDS"][b, 3]
    arcpy.CalculateField_management(feature_class, new_attribute_name, from_attribute)

    return

def SelectFeatures(input_xls, input_302gdb, input_gdb_302workdir, input_26gdb, input_mxd):

    mxd = arcpy.mapping.MapDocument(input_mxd)
    mapLayers = arcpy.mapping.ListLayers(mxd)

    # defines excel document
    xc = xls_class()
    xc.read(input_xls)

    # creates a list of queries to perform on the shapefile

    print("Running query list on all layers")
    for layer in mapLayers:
        desc = arcpy.Describe(layer)
        print("Querying {0}".format(desc.name))
        b = 1
        while b < 240:

            try:
                geo= xc.worksheets["CAD_SDS"][b, 1]
                ln = xc.worksheets["CAD_SDS"][b, 4]
                lv = xc.worksheets["CAD_SDS"][b, 5]
                co = xc.worksheets["CAD_SDS"][b, 6]
                lt = xc.worksheets["CAD_SDS"][b, 7]
                lw = xc.worksheets["CAD_SDS"][b, 9]
                ref = xc.worksheets["CAD_SDS"][b, 0]

                if lv != "":
                    lv = int(lv)

                if co != "":
                    co = int(co)

                if lw != "":
                    lw = int(lw)

                if ref == "" or geo  == "line" or geo == "line 3d":
                    query = """"LAYER" = '{0}' AND "LEVEL" = {1} AND "COLOR" = {2} AND "LINETYPE" = '{3}' AND "LYRLINEWT" = {4}""".format(ln, lv, co, lt, lw)
                else:
                    query = """"LAYER" = '{0}' AND "LEVEL" = {1} AND "COLOR" = {2} AND "LINETYPE" = '{3}' AND "LYRLINEWT" = {4} AND "REFNAME" = '{5}'""".format(ln, lv, co, lt, lw, ref)

                out_SDS = xc.worksheets["CAD_SDS"][b, 12]
                out_FC = xc.worksheets["CAD_SDS"][b, 13]
                out_name = out_SDS + "\\" + out_FC

                if out_SDS == "":
                    out_SDS = xc.worksheets["CAD_SDS"][b, 14]
                    out_FC = xc.worksheets["CAD_SDS"][b, 15]
                    out_name = out_SDS + "\\" + out_FC

                print out_FC
                print query

                if xc.worksheets["CAD_SDS"][b, 13] != "" :
                    outdir = input_302gdb
                    # for shapefiles that do not already exists
                    if os.path.exists(os.path.join(outdir, out_name)):
                        # apply the query to select specific attributes
                        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                        # add to existing layer
                        arcpy.Append_management(layer, os.path.join(outdir, out_name))

                        # calculate description attribute
                        CreateFieldFromXLSX(out_name, "Description")

                    # for shapefiles that do not exist
                    else:
                        # pull the spatial reference information
                        spat_ref = arcpy.Describe(outdir + "\\" + out_FC).spatialReference

                        # create an empty new featureclass
                        arcpy.CreateFeatureclass_management(outdir, out_name, "POLYGON", spatial_reference = spat_ref)

                        # apply the query to select specific attributes
                        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                         # make new layer
                        arcpy.FeatureClassToFeatureClass_conversion(layer, outdir, out_name)

                        # calculate description attribute
                        CreateFieldFromXLSX(out_name, "Description")

                else:
                    outdir = input_26gdb
                    if not os.path.exists(os.path.join(outdir, out_name)):

                        # pull the spatial reference information
                        spat_ref = arcpy.Describe(outdir + "\\" + out_FC).spatialReference

                        # create an empty new featureclass
                        arcpy.CreateFeatureclass_management(outdir, out_name, "POLYGON", spatial_reference = spat_ref)

                        # apply the query to select specific attributes
                        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                         # make new layer
                        arcpy.FeatureClassToFeatureClass_conversion(layer, outdir, out_name)

                        # calculate description attribute
                        CreateFieldFromXLSX(out_name, "Narrative")

                    # for shapefiles that do exist
                    else:
                        # apply the query to select specific attributes
                        arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                        # add to existing layer
                        arcpy.Append_management(layer, os.path.join(outdir, out_name))
                        # make new layer
                        arcpy.FeatureClassToFeatureClass_conversion(layer, outdir, out_name)

                        # calculate description attribute
                        CreateFieldFromXLSX(out_name, "Narrative")

                print out_name + " exported"

            except:
                print("==== this is clearly Will's fault ====")

            b += 1

    return

if __name__ == "__main__":

    # laurens test area
    gdb302 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    gdb26 = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_26_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    gdbdir = "CAD_Temporary"
    mxd = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd"
    xls = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Modified_Cad_Label_to_SDS.xlsx"
    SelectFeatures(xls, gdb302, gdbdir, gdb26, mxd)

    # jeffs test area
    #gdb    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    #gdbdir = "CAD_Temporary"
    #mxd    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\5637_testspace.mxd"
    #xls    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\Cad_Label_to_SDS.xlsx"
    #outdir = gdb
    #SelectFeatures(xls, gdb, gdbdir, mxd, outdir)
