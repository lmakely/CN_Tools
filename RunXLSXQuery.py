__author__ = 'lmakely'

from xls_class import xls_class
import arcpy
import os
arcpy.env.overwriteOutput = True

def CreateFieldFromXLSX(b, in_table, feature_class, new_attribute_name):

    xc = xls_class()
    xc.read(in_table)

    field_names = []
    fields      = arcpy.ListFields(feature_class)

    # get list of current fields
    for field in fields:
        field_names.append(field.baseName)

    # make description field
    if new_attribute_name not in field_names:
        arcpy.AddField_management(feature_class, new_attribute_name, "TEXT")
        print("Added '{0}' attribute".format(new_attribute_name))

    from_attribute = xc.worksheets["CAD_SDS"][b, 3]
    print "Calculating attribute as: " + from_attribute
    expression = "[DESCRIP] = '" + from_attribute + "'"
    arcpy.CalculateField_management(feature_class, new_attribute_name, expression)

    return

def SelectFeatures(input_xls, input_gdb, input_gdb_workdir, input_mxd, outdir):

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
        geo = xc.worksheets["CAD_SDS"][b, 1]
        while b < 240:
            try:
                ln = xc.worksheets["CAD_SDS"][b, 4]
                lv = xc.worksheets["CAD_SDS"][b, 5]
                co = xc.worksheets["CAD_SDS"][b, 6]
                lt = xc.worksheets["CAD_SDS"][b, 7]
                lw = xc.worksheets["CAD_SDS"][b, 9]
                ref = xc.worksheets["CAD_SDS"][b, 0]

                # ensures that inputs are integers and not floats
                if lv != "":
                    lv = int(lv)

                if co != "":
                    co = int(co)

                if lw != "":
                    lw = int(lw)

                if lt == "No Value" or lt == "FALSE":
                    lt = ""

                #formatting strings
                #layer name
                if ln == "":
                    lnstring = ""
                else:
                    lnstring = (""""LAYER" = '{0}'""").format(ln)
                #level
                if lv == "":
                    lvstring = ""
                else:
                    lvstring = (""" AND "LEVEL" = {0}""").format(lv)
                #color
                if co =="":
                    costring = ""
                else:
                    costring = (""" AND "COLOR" = {0}""").format(co)
                #linetype
                if lt == "":
                    ltsring = ""
                else:
                    ltstring = (""" AND "LINETYPE" = '{0}'""").format(lt)
                
                if lw == "":
                    lwstring = ""
                else:
                    lwstring = (""" AND "LYRLINEWT" = {0}""").format(lw)

                if ref == "":
                    refname = ""
                else:
                    refname = (""" AND "REFNAME" = '{0}'""").format(ref)

                #building query
                query = """{0}{1}{2}{3}{4}{5}""".format(lnstring, lvstring, costring, ltstring, lwstring, refname)

                out_name = xc.worksheets["CAD_SDS"][b, 12].replace("_","")

                print("Searching feature class: " + out_name)
                output = os.path.join(outdir, out_name + ".shp")
                print output
                print query

                # for shapefiles that do not already exists
                if not os.path.exists(os.path.join(outdir, out_name)):

                    # pull the spatial reference information
                    spat_ref = arcpy.Describe(input_gdb + "\\" + input_gdb_workdir).spatialReference

                    # create an empty new featureclass
                    arcpy.CreateFeatureclass_management(outdir, out_name, "POLYGON", spatial_reference = spat_ref)

                    
                    # apply the query to select specific attributes
                    selection = arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                    # make new layer
                    arcpy.FeatureClassToFeatureClass_conversion(layer, outdir, out_name)

                    # calculate description attribute
                    CreateFieldFromXLSX(b, input_xls, output, "Descrip")
                    
                # for shapefiles that do exist
                else:

                    # apply the query to select specific attributes
                    arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)

                    # add to existing layer
                    arcpy.Append_management(layer, os.path.join(outdir, out_name))

                    # calculate description attribute
                    CreateFieldFromXLSX(b, input_xls, output, "Descrip")
                    
                print("---------------------------------------------")
                print              out_name + " exported"
                print("---------------------------------------------")
##
##                if "Lines" in desc.name:
##                    if "line" in geo:
##                        if lv != "":
##                            lv = int(lv)
##
##                        if co != "":
##                            co = int(co)
##
##                        if lw != "":
##                            lw = int(lw)
##
##                        if lt == "No Value" or lt == "FALSE":
##                            lt = ""
##
##                        #formatting strings
##                        #layer name
##                        if ln == "":
##                            lnstring = ""
##                        else:
##                            lnstring = (""""LAYER" = '{0}'""").format(lv)
##                        #level
##                        if lv == "":
##                            lvstring = ""
##                        else:
##                            lvstring = (""" AND "LEVEL" = {0}""").format(lv)
##                        #color
##                        if co =="":
##                            costring = ""
##                        else:
##                            costring = (""" AND "COLOR" = {0}""").format(co)
##                        #linetype
##                        if lt == "":
##                            ltsring = ""
##                        else:
##                            ltstring = (""" AND "LINETYPE" = '{0}'""").format(lt)
##                        
##                        if lw == "":
##                            lwstring = ""
##                        else:
##                            lwstring = (""" AND "LYRLINEWT" = {0}""").format(lw)
##
##                        if ref == "":
##                            refname = ""
##                        else:
##                            refname = (""" AND "REFNAME" = {0}""").format(ref)
##
##                        #building query
##                        query = """{0}{1}{2}{3}{4}{5}""".format(lnstring, lvstring, costring, ltstring, lwstring, refname)
##
##                        out_name = xc.worksheets["CAD_SDS"][b, 12].replace("_","")
##
##                        print("Searching feature class: " + out_name)
##                        output = os.path.join(outdir, out_name + ".shp")
##                        print output
##                        print query
##
##                        # for shapefiles that do not already exists
##                        if not os.path.exists(os.path.join(outdir, out_name)):
##
##                            # pull the spatial reference information
##                            spat_ref = arcpy.Describe(input_gdb + "\\" + input_gdb_workdir).spatialReference
##
##                            # create an empty new featureclass
##                            arcpy.CreateFeatureclass_management(outdir, out_name, "POLYLINE", spatial_reference = spat_ref)
##
##                            # apply the query to select specific attributes
##                            arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)
##
##                            # make new layer
##                            arcpy.FeatureClassToFeatureClass_conversion(layer, outdir, out_name)
##
##                            # calculate description attribute
##                            CreateFieldFromXLSX(b, input_xls, output, "Descrip")
##                            
##                        # for shapefiles that do exist
##                        else:
##
##                            # apply the query to select specific attributes
##                            arcpy.SelectLayerByAttribute_management(layer, "NEW_SELECTION", query)
##
##                            # add to existing layer
##                            arcpy.Append_management(layer, os.path.join(outdir, out_name))
##
##                            CreateFieldFromXLSX(b, input_xls, output, "Descrip")
##
##                        print("---------------------------------------------")
##                        print              out_name + " exported"
##                        print("---------------------------------------------")
##
##
##                elif "point" in geo:
##                    print "Point feature. Skipping..."

                
            except:
                print "-------------------------------------------------------------------"
                print "                     No selection was made"
                print "-------------------------------------------------------------------"
            b += 1
    return



if __name__ == "__main__":

    # laurens test area
    gdb = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    gdbdir = "CAD_Temporary"
    mxd = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\5637_testspace.mxd"
    xls = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\Cad_Label_to_SDS.xlsx"
    outdir = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\LMM\shps2"
    SelectFeatures(xls, gdb, gdbdir, mxd, outdir)

    # jeffs test area
    # gdb    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\NDM_302_Schema_UTM33_EGM08_GaetaSE_working\NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb"
    # gdbdir = "CAD_Temporary"
    # mxd    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\5637_testspace.mxd"
    # xls    = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\Cad_Label_to_SDS.xlsx"
    # outdir = gdb
    # SelectFeatures(xls, gdb, gdbdir, mxd, outdir)
