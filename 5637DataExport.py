#-------------------------------------------------------------------------------
# Name:        5637DataExport
# Purpose:     Used for the seperation and exportation of data from a GDB to
#              predefined feature classes
#
# Author:      wmunsell
#
# Created:     15/06/2015
# Copyright:   (c) wmunsell 2015
# Licence:     <your licence>
#-------------------------------------------------------------------------------
import arcpy
import os
import sys
from arcpy import env

arcpy.env.overwriteOutput = True
MXD = arcpy.mapping.MapDocument(r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\WUM\Capodichino2.mxd")
mapLayers = arcpy.mapping.ListLayers(MXD)

fileLocation = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\WUM\DGN Conversion\yourFace"
fileName = "testYourFace"

selection1 = """ "Entity" = 'Closed Shape' """
selection2 = """ "Entity" <> 'Closed Shape' """

tempConversion = r"V:\Projects\5637-GIS JV - Aerial Mapping for NSA Naples\Development\Working\WUM\DGN Conversion\yourFace\testYourFace.gdb"

newGDB = arcpy.CreateFileGDB_management (fileLocation, fileName)
anno = arcpy.CreateFeatureclass_management(newGDB, "Annotation", "POINT")
point = arcpy.CreateFeatureclass_management(newGDB, "Points", "POINT")
line = arcpy.CreateFeatureclass_management(newGDB, "Lines", "POLYLINE")
poly = arcpy.CreateFeatureclass_management(newGDB, "Polygons", "POLYGON")


for layer in mapLayers:
    desc = arcpy.Describe(layer)
    print desc.name
    if desc.name.lower() == "annotation":
        arcpy.FeatureToPoint_management(layer, anno)
    if desc.name.lower() == "point":
        arcpy.CopyFeatures_management(layer, point)
    if desc.name.lower() == "polyline":
        tempLine = arcpy.CreateFeatureclass_management(newGDB, "tempLines", "POLYLINE")
        select = arcpy.Select_analysis (layer, tempLine, selection1)
        tempPoly = arcpy.FeatureToPolygon_management(tempLine, poly, "", "ATTRIBUTES", anno)
        arcpy.Delete_management (tempLine)
        arcpy.Select_analysis (layer, line, selection2)
    if desc.name.lower() == "polygon":
        arcpy.Append_management(layer, poly, "NO_TEST")
    if desc.name.lower() == "multipatch":
        arcpy.Append_management(layer, poly, "NO_TEST")

print "Script Complete"