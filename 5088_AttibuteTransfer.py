__author__ = 'lmakely'


import arcpy
import shutil
import os


# this function adds up numbers from points shp that intersect a polygon in a shp
# inserts number into polygon shp
def SumAttibuteAndUpdatePolygon():
    if PPV_Unit_Number

# identifies the lowest identifying number in a set of points inside a shapefile
# sets street number to that number and then calculates Mailing_Address and sdsfeaturedescription
# working on how to identify PPV unit number that need to be identified.
def IdentifyLowestNumber():


# Adds up the number of points that lie within a polygon and updates Facility_Unit_Quantity
def SumPointsAndUpdatePolygon():



# Runs all three scripts
def AttributeTransfer():
    print "     Beginning to calculate facility bedrooms, bathrooms, and half-baths"
    SumAttibuteAndUpdatePolygon()
    print "     Completed updating the bedrooms, bathrooms, and half-bath counts"
    print "-------------------------------------------------------------------------"
    print "     Beginning to identify the lowest address number"
    IdentifyLowestNumber()
    print "     Completed updating the lowest addresses"
    print "-------------------------------------------------------------------------"
    print "     Beginning to calculate the Facility_Unit_Quantity"
    SumPointsAndUpdatePolygon()
    print "     Completed updating the Facility_Unit_Quantity"
    print "-------------------------------------------------------------------------"


# testing area
if __name__ == "__main__":

    workspace = r"C:\LMM\5088\AttributeTesting"
    gdb = r"C:\LMM\5088\AttributeTesting\HI.gdb"
    mxd = r"C:\LMM\5088\AttributeTesting\5088_AttributeTesting.mxd"

    AttributeTransfer (workspace, mxd)
