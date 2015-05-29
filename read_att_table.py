
import arcpy
import shutil
import os


def backup_shapefile(source_shp):
    """ copies a shapefile and all its metadata """

    metalist = [".cpg", ".dbf", ".prj", ".sbn", ".sbx", ".shp.xml" ,".shx"]
    head, tail = os.path.split(source_shp)

    copylist = [source_shp]
    for metaitem in metalist:
        copylist.append(source_shp.replace(".shp",metaitem))

    # create backupdir
    backupdir = os.path.join(head,"{0}_backup".format(tail.replace(".shp","")))
    if os.path.isdir(backupdir):
        shutil.rmtree(backupdir)
        os.makedirs(backupdir)
    else:
        os.makedirs(backupdir)

    # copy files into the directory
    for copy in copylist:
        shutil.copy(copy, os.path.join(backupdir, os.path.basename(copy)))

    print("Backup created at {0}".format(backupdir))
    return
    
    
def att_table_to_tdo(shp_filepath):
    """
    Returns a python table of input shapefiles attribute table
    """

    # create a backup of the shapefile
    backup_shapefile(shp_filepath)
    
    # find the field names
    field_names = []
    fields      = arcpy.ListFields(shp_filepath)

    print("Shapefile has the following fields:")
    for field in fields:
        print field.baseName
        field_names.append(field.baseName)
        
    # add new fields if desired
    if "Monkey" not in field_names:
        arcpy.AddField_management(shp_filepath, "Monkey", field_type = "text")

    # build iterator by each row (this is where the cool stuff goes)
    rows = arcpy.UpdateCursor(shp_filepath)

    for row in rows:
        FeatureID = getattr(row, "FeatureID")
        setattr(row, "Monkey" ,"baboon")
        rows.updateRow(row)

    return 


# testing area
if __name__ == "__main__":

    shapefile = r"C:\Users\jwely\Desktop\troubleshooting\Lauren_att_table\RAW\UP.shp"
    
    att_table_to_tdo(shapefile)













    
    
