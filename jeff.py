
import arcpy

def new_shape_by_query(shp_filepath, query_dict):


    field_names = []
    fields      = arcpy.ListFields(shp_filepath)

    print("Shapefile has the following fields:")
    for field in fields:
        print field.baseName
        field_names.append(field.baseName)

    # add new fields if desired
    #arcpy.AddField_management(shp_filepath, "MediaPath", field_type = "text")
    # build iterator by each row (this is where the cool stuff goes)
    rows = arcpy.UpdateCursor(shp_filepath)

    for row in rows:
        FeatureID = getattr(row, "FeatureID")
        rows.updateRow(row)
        pass
    return


if __name__ == "__main__":

    gdb = '''C:/Users/Jeff/Desktop/Github/CN_Tools/Reference/
            NDM_302_Schema_UTM33_EGM08_GaetaSE_working/NDM_302_Schema_UTM33_EGM08_GaetaSE_working.gdb/CAD_Polygons_Gaeta_SE'''
    shp = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\shapeversion\Export_Output.shp"
    xls = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\Cad_Label_to_SDS.xlsx"
    mxd = r"C:\Users\Jeff\Desktop\Github\CN_Tools\Reference\5637_testspace.mxd"

    query = {"RefName": "A",
             "Level": "VA_ROAD_EASP",
             "COLOR": 0,
             "Linetype": "LongDashed"
             "Level
    new_shape_by_query(shp, )