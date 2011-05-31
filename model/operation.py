# -*- coding: utf-8 -*-
#
# LegoERP, make software yourself
#
# Copyright (C) 2011, Kevin Pouget
#
# LegoERP is free software; you can redistribute it and/or modify it under
# terms of the  GNU General Public License as published  by the Free Soft-
# ware  Foundation;  either version 2,  or (at your option) any later ver-
# sion.  LegoERP is distributed  in the hope that it  will be useful,  but
# WITHOUT ANY WARRANTY; without even the implied warranty of MERCHANTABIL-
# ITY or  FITNESS FOR A  PARTICULAR PURPOSE.  See the GNU  General  Public
# License for  more details.  You should have  received  a copy of the GNU
# General Public License  along with this  program;  If not,  write to the
# Free Software Foundation,  51 Franklin Street,  Fifth Floor,  Boston  MA
# 02110-1301, USA.
#
# File: operation.py

from django import forms

from couch import MetaLegoDocument, ViewField, TextField, IntegerField, OneToOneField, OneToManyField
from datatype import DataType, DataTypeField, DataTypeFieldAdress, DataTypeFieldString
from datatype import DataTypeFieldFloat, DataTypeFieldInteger, DataTypeFieldRelation


class Operation(MetaLegoDocument):
    """
    Description of an operation on the database.
    Typically, an operation is a set of updates
    on a single or a set of database documents.
	"""

    __decls__ = { 'DataType'              : DataType,
                  'DataTypeFieldAdress'   : DataTypeFieldAdress,
                  'DataTypeFieldString'   : DataTypeFieldString,
                  'DataTypeFieldFloat'    : DataTypeFieldFloat,
                  'DataTypeFieldInteger'  : DataTypeFieldInteger,
                  'DataTypeFieldRelation' : DataTypeFieldRelation }

    datatype = OneToOneField(DataType)

    def __init__(self, database=None, label=None, **kwords):
        super(Operation, self).__init__(database=database,
                                        label=label,
                                        **kwords)
        
        if not self.__decls__.has_key('UpdateDataOperation'):
            self.__decls__['UpdateDataOperation'] = UpdateDataOperation
            self.__decls__['AddDataOperation'] = AddDataOperation
            self.__decls__['DelDataOperation'] = DelDataOperation

    def at_list_level(self):
        if isinstance(self, AddDataOperation):
            return True
        return False
    
    def form(self, fields=None, content=None, post=None):
        if not fields:
            fields = self.form_fields()

        options = { 'fields' : fields }
        if content:
            options['initial'] = content
        if post:
            return OperationForm(post, **options)

        return OperationForm(**options)


class UpdateDataOperation(Operation):

    css_class = 'update_project'

    updatefields = OneToManyField(DataTypeField)

    def __init__(self, database=None, label=None, **kwords):
        super(UpdateDataOperation, self).__init__(database=database,
                                                  label=label,
                                                  **kwords)

    def form_fields(self):
        return self.updatefields


class AddDataOperation(Operation):

    css_class = 'new_repository'

    displayedfields = OneToManyField(DataTypeField)
    fixedfields     = OneToManyField(DataTypeField)

    def __init__(self, database=None, label=None, **kwords):
        super(AddDataOperation, self).__init__(database=database,
                                               label=label,
                                               **kwords)

    def form_fields(self):
        return self.displayedfields


class DelDataOperation(Operation):

    css_class = 'delete_repository'

    def __init__(self, database=None, label=None, **kwords):
        super(DelDataOperation, self).__init__(database=database,
                                               label=label,
                                               **kwords)

    def form_fields(self):
        return None


class OperationForm(forms.Form):

    def __init__(self, *args, **kwargs):
        fields = kwargs.pop('fields')

        if kwargs.has_key('initial'):
            initial = kwargs.pop('initial')
        else:
            initial = {}

        forms.Form.__init__(self, *args, **kwargs)

        for field in fields:
            # Beurk ?
            if (isinstance(field, DataTypeFieldString) or 
                isinstance(field, DataTypeFieldAdress)):
                self.fields[field.id] = forms.CharField(label=field.label,
                                                        initial=initial.get(field.id))

            elif isinstance(field, DataTypeFieldFloat):
                self.fields[field.id] = forms.FloatField(label=field.label,
                                                         initial=initial.get(field.id))

            elif isinstance(field, DataTypeFieldInteger):
                self.fields[field.id] = forms.IntegerField(label=field.label,
                                                           initial=initial.get(field.id))

            #self.fields[field.id].widget.attrs['disabled'] = 'disabled'