# -*- coding: utf-8 -*-
__title__   = "Room name + number \n to parameter"
__author__     = "Sean De Gent"
__doc__ = """Version = 1.0
Date    = 22-09-23
_____________________________________________________________________
Description:

kopieer de room name & room number in een parameter naar keuze

*** Keuze parameter nog nakijken***
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

for room in all_rooms:
    param_set = room.Parameters
# for e in all_elements:
#     param_set = e.Parameters


unique_param_names = []

for param in param_set:
    param_name = param.Definition.Name
    param_set_type = param.StorageType


    if param_set_type == StorageType.String:
        # Voeg de parameter naam toe aan de set als deze nog niet is opgenomen
        if param_name not in unique_param_names:
            unique_param_names.append(param_name)
            # print("Parameter naam : {}".format(param_name))


value = SelectFromList('Select parameter', unique_param_names)


# Start een transactie om wijzigingen in het document aan te brengen
t = Transaction(doc, "room name to parameter")
t.Start()

try:
    for room in all_rooms:
        room_name = room.get_Parameter(BuiltInParameter.ROOM_NAME).AsValueString()
        room_number = room.get_Parameter(BuiltInParameter.ROOM_NUMBER).AsValueString()
        room_info = room_number + " - " + room_name
        print(room_name)
        room_bounding_box = room.get_BoundingBox(None)
        outline = Outline(room_bounding_box.Min,room_bounding_box.Max)
        bb_filter = BoundingBoxIntersectsFilter(outline)

        # Verzamel alle elementen die de filtercriteria matchen (die zich binnen de mass bevinden)
        host_elements = FilteredElementCollector(doc).WherePasses(
            bb_filter).WhereElementIsNotElementType().ToElements()

        for host_element in host_elements:
            host_element_param = host_element.LookupParameter(value)
            if host_element_param:
                current_value = host_element_param.AsString()  # Of gebruik .AsValueString(), afhankelijk van het parametertype

                # Controleer of de huidige waarde niet is ingesteld of niet overeenkomt met de mass_zone_value
                if not host_element_param.IsReadOnly and (
                        current_value is None or current_value != room_info):
                    host_element_param.Set(room_info)

except Exception as e:
    print("Exception: {}".format(e))
    t.RollBack()
else:
    t.Commit()
#
#
#
# print(value)
# for room in all_rooms:
#     room_parameter = room.Parameters
#     for param in room_parameter:
#         param_name = param.Definition.Name
#         param_value = None
#         print(room)