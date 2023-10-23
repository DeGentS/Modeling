# -*- coding: utf-8 -*-
__title__   = "Copy Level Name \n to Mark Parameter"
__doc__     = """Here put text"""

#-----------------------IMPORTS-------------------------------------------------------
#IMPORTS
import clr
import os
import sys
import System
import shutil

# Import Revit API elements
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import BuiltInCategory as Bic
from pyrevit import revit
from rpw.ui.forms import SelectFromList
from System.Collections.Generic import List

#----------------------VARIABLES--------------------------------------------------------
doc         = __revit__.ActiveUIDocument.Document
uidoc       = __revit__.ActiveUIDocument
app         = __revit__.Application

# Function to get the associated level based on Z location
def get_level_by_elevation(elevation, levels):
    for level in reversed(levels):  # Start from the highest level
        if elevation >= level.Elevation:
            return level
    return None

# Retrieve and sort levels based on their elevations
levels = FilteredElementCollector(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()
levels = sorted(levels, key=lambda x: x.Elevation)

all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

# Start a transaction since we're modifying elements
with Transaction(doc, "Copy Level Name to Mark") as t:
    t.Start()

    for elem in all_elements:
        associated_level_name = None

        # First, try to get the level using LevelId
        if hasattr(elem, "LevelId") and elem.LevelId != ElementId.InvalidElementId:
            associated_level_name = doc.GetElement(elem.LevelId).get_Parameter(BuiltInParameter.DATUM_TEXT).AsValueString()

        # If LevelId didn't work, try to get the level from the "Schedule Level" parameter
        if not associated_level_name:
            schedule_level_param = elem.LookupParameter("Schedule Level")
            if schedule_level_param:
                associated_level_name = schedule_level_param.AsValueString()

        # If the element doesn't have a direct association with a level, check if it's hosted and get its host's level
        if not associated_level_name and hasattr(elem, "Host"):
            host = elem.Host
            if host and host.LevelId != ElementId.InvalidElementId:
                associated_level_name = doc.GetElement(host.LevelId).get_Parameter(BuiltInParameter.DATUM_TEXT).AsValueString()

        # If no associated level found, try using the Z location
        if not associated_level_name:
            bbox = elem.get_BoundingBox(None)
            if bbox:
                base_z = bbox.Min.Z  # Get the minimum Z value of the bounding box
                level = get_level_by_elevation(base_z, levels)
                if level:
                    associated_level_name = level.Name

        # If we found an associated level, set the Mark parameter
        if associated_level_name:
            mark_param = elem.LookupParameter("Mark")
            if mark_param:
                mark_param.Set(associated_level_name)

    t.Commit()
