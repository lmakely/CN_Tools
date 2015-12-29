__author__ = 'lmakely'


import arcpy
import shutil
import os


# this function adds up numbers from points shp that intersect a polygon in a shp
# inserts number into polygon shp
def AddUpBBHBs():


# identifies the lowest identifying number in a set of points inside a shapefile
# sets street number to that number and then calculates mailing address and sds feature description
# working on how to identify PPV unit number that need to be identified. 
def LowestAddress():


def SumUnits():


def AttributeTransfer():
    AddUpBBHBs()
    LowestAddress()
    SumUnits()

# testing area
if __name__ == "__main__":

    workspace = r"C:\LMM\5088\AttributeTesting"
    gdb = r"C:\LMM\5088\AttributeTesting\HI.gdb"
    mxd = r"C:\LMM\5088\AttributeTesting\5088_AttributeTesting.mxd"

    AttributeTransfer (workspace, mxd)
