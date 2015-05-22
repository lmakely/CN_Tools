# author: Lauren Makely
# organization: Clark Nexsen
# date: May 19, 2015

from dnppy import core
import arcpy
import os

works = "V:\\Projects\\5646_GAARNG_SUE_Survey_RC\\Development\\Working\\LMM"

arcpy.env.workspace = "V:\\Projects\\5646_GAARNG_SUE_Survey_RC\\Development\\Working\\LMM"

clipfiles = core.list_files(False, works, ".shp",[".prj", ".clf", '.dbf', '.sbx', '.sbn', '.shx', '.xml'])

for i in clipfiles:
    head, tail = os.path.split(i)
    clipto = works + "\\Cedartown_Inst.shp"
    outs = "V:\\Projects\\5646_GAARNG_SUE_Survey_RC\\Development\\Working\\LMM\\Clipped" + "\\" + tail
    cluster_tolerance="#"
    arcpy.Clip_analysis(i,clipto,outs,cluster_tolerance)

    # Help: batch clips features to a defined shape
    #   workspace   folder with data to be clipped
    #   outspace    folder for clipped data to be placed
    #   clipto      file to clip features to with extension
    #   tolerance   cluster tolerance which is optional (use "#") if no input

def batch_clip(workspace,outspace, clipto, tolerance):
    from dnppy import core
    import arcpy
    import os
    arcpy.env.workspace = workspace

    clipfiles = core.list_files(False, works, ".shp",[".prj", ".clf", '.dbf', '.sbx', '.sbn', '.shx', '.xml'])
    for i in clipfiles:
        head, tail = os.path.split(i)
        clipfile = works + "\\" + clipto
        outs = outspace + "\\" + tail[:-4] + "_Clip.shp"
        cluster_tolerance= tolerance
        print "Currently clipping " + tail
        arcpy.Clip_analysis(i,clipto,outs,cluster_tolerance)
        print tail + " clipped!"
