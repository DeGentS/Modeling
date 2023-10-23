# -*- coding: utf-8 -*-
__title__   = "Select elements \n of level"
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

#----------------------MAIN--------------------------------------------------------
#MAIN

levels = FilteredElementCollector(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()
all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

level_list = []

for level in levels:
    level_name = level.get_Parameter(BuiltInParameter.DATUM_TEXT).AsValueString()
    level_list.append(level_name)

value = SelectFromList('Select level', level_list)

element_ids = List[ElementId]()


for elem in all_elements:
    associated_level_name = None

    # First, try to get the level using LevelId
    if hasattr(elem, "LevelId") and elem.LevelId != ElementId.InvalidElementId:
        associated_level_name = doc.GetElement(elem.LevelId).get_Parameter(BuiltInParameter.DATUM_TEXT).AsValueString()

    # If LevelId didn't work, try to get the level from the "Schedule Level" parameter
    if not associated_level_name:
        schedule_level_param = elem.LookupParameter("Schedule Level")  # Adjust "Schedule Level" if the parameter has a different name in your setup
        if schedule_level_param:
            associated_level_name = schedule_level_param.AsValueString()

    # If the element doesn't have a direct association with a level, check if it's hosted and get its host's level
    if not associated_level_name and hasattr(elem, "Host"):
        host = elem.Host
        if host and host.LevelId != ElementId.InvalidElementId:
            associated_level_name = doc.GetElement(host.LevelId).get_Parameter(BuiltInParameter.DATUM_TEXT).AsValueString()

    # Compare the obtained level name to the selected level
    if value == associated_level_name:
        element_id = elem.Id
        element_ids.Add(element_id)

uidoc.Selection.SetElementIds(element_ids)
