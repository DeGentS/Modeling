# -*- coding: utf-8 -*-
__title__ = "Element ID" \
            " to Mark "                  # Name of the button displayed in Revit UI
__doc__ = """Version = 1.0
Date    = 14.06.2023
_____________________________________________________________________
Description:

This tool will copy the element id to the parameter Mark.
_____________________________________________________________________
How-to:

-> Click on the button

_____________________________________________________________________
Last update:
- [14.06.2023] - 1.0 RELEASE
_____________________________________________________________________
To-Do:
_____________________________________________________________________
Author: Sean De Gent"""                                                      # Button Description shown in Revit UI

import clr
clr.AddReference('RevitAPI')
from Autodesk.Revit.DB import FilteredElementCollector, BuiltInParameter, Transaction
from itertools import count

# Get the active document
doc = __revit__.ActiveUIDocument.Document

# Start a transaction
transaction = Transaction(doc, "Copy Element ID to Mark")
transaction.Start()

# Collect all elements in the document
collector = FilteredElementCollector(doc)
elements = collector.WhereElementIsNotElementType().ToElements()
element_count = len(elements)

# Loop through each element and copy Element ID to Mark parameter
for element in elements:
    if element.LookupParameter("Mark"):
        element_id = element.Id.IntegerValue
        element.LookupParameter("Mark").Set(str(element_id))
print("succes")
print(element.LookupParameter("Mark"))

print(element_count)
# Commit the transaction
transaction.Commit()
