# -*- coding: utf-8 -*-
__title__   = "Room \n to element"
__author__     = "Sean De Gent"
__doc__ = """Version = 1.0
Date    = 22-09-23
_____________________________________________________________________
Description:

kopieer de room name in de parameter  BPL_Room in elk element
_____________________________________________________________
Last update:

- [22-09-23] 1.0 RELEASE


author  = Sean De Gent i.o.v. BimPlan

_____________________________________________________________________
"""
#-----------------------IMPORTS-------------------------------------------------------
#IMPORTS
import clr
import os
import sys
import System
import shutil


# Importeren van Revit API-elementen
clr.AddReference("RevitAPI")
import Autodesk
from Autodesk.Revit.DB import *
from Autodesk.Revit.DB import BuiltInCategory as Bic
from rpw.ui.forms import SelectFromList

# #----------------------VARIABLES--------------------------------------------------------
# #VARIABLES
#
doc         = __revit__.ActiveUIDocument.Document
uidoc       = __revit__.ActiveUIDocument
app         = __revit__.Application

#----------------------MAIN--------------------------------------------------------
#MAIN


levels = FilteredElementCollector(doc).OfCategory(Bic.OST_Levels).WhereElementIsNotElementType().ToElements()
all_rooms = FilteredElementCollector(doc).OfCategory(Bic.OST_Rooms).WhereElementIsNotElementType().ToElements()
all_elements = FilteredElementCollector(doc).WhereElementIsNotElementType().ToElements()

# Start een transactie om wijzigingen in het document aan te brengen
t = Transaction(doc, "room name to parameter")
t.Start()

try:
    for room in all_rooms:
        room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
        print(room_name)
        room_bounding_box = room.get_BoundingBox(None)
        outline = Outline(room_bounding_box.Min,room_bounding_box.Max)
        bb_filter = BoundingBoxIntersectsFilter(outline)

        # Verzamel alle elementen die de filtercriteria matchen (die zich binnen de mass bevinden)
        host_elements = FilteredElementCollector(doc).WherePasses(
            bb_filter).WhereElementIsNotElementType().ToElements()

        for host_element in host_elements:
            host_element_param = host_element.LookupParameter("BPL_Room")
            if host_element_param:
                current_value = host_element_param.AsString()  # Of gebruik .AsValueString(), afhankelijk van het parametertype

                # Controleer of de huidige waarde niet is ingesteld of niet overeenkomt met de mass_zone_value
                if not host_element_param.IsReadOnly and (
                        current_value is None or current_value != room_name):
                    host_element_param.Set(room_name)

except Exception as e:
    print("Exception: {}".format(e))
    t.RollBack()
else:
    t.Commit()
