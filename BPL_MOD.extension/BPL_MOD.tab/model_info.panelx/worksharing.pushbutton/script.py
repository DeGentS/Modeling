# -*- coding: utf-8 -*-
__title__   = "Worksharing?"
__doc__     = """Here put text"""

#-----------------------IMPORTS-------------------------------------------------------
from pyrevit import forms, script

#----------------------VARIABLES--------------------------------------------------------
doc = script.get_document()  # Gets the current active document

#----------------------MAIN--------------------------------------------------------
forms.check_workshared(doc=doc, message='Model is not workshared.')
