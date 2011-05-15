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
# File: datatype.py

from couch import *

from django import forms


class DataTypeForm(forms.Form):

    def __init__(self, *args, **kwargs):
        datatype = kwargs.pop('datatype')
        
        if kwargs.has_key('initial'):
            initial = kwargs.pop('initial')
        else:
            initial = {}

        forms.Form.__init__(self, *args, **kwargs)

        for field in datatype.fields:
            # Beurk ?
            if (isinstance(field, StringDataTypeField) or 
                isinstance(field, AdressDataTypeField)):
                self.fields[field.id] = forms.CharField(label=field.label,
                                                        initial=initial.get(field.id))

            elif isinstance(field, FloatDataTypeField):
                self.fields[field.id] = forms.FloatField(label=field.label,
                                                         initial=initial.get(field.id))

            elif isinstance(field, IntegerDataTypeField):
                self.fields[field.id] = forms.IntegerField(label=field.label,
                                                           initial=initial.get(field.id))

            #self.fields[field.id].widget.attrs['disabled'] = 'disabled'

class DataType(MetaLegoDocument):
    """
    Description of a database document type.
    """

    with_fields = ViewField(design='datatype',
                            wrapper=None,
                            map_fun='''\
                   function(doc) {
                       if (doc.metatype == 'DataType') {
                           emit([doc._id, 0], doc);
                       } else if (doc.metatype.indexOf('DataTypeField') > -1) {
                           emit([doc.datatype, doc.rank], doc);
                       }
                   }''')

    fields = None

    def __init__(self, database=None, label=None, fields=[]):
        super(DataType, self).__init__()

        self.fields = []
        if database:
            self.label = label
            self.store(database)

            rank = 1
            for field in fields:
                field.rank = rank
                field.datatype = self.id
                field.store(database)
                self.fields.append(field)
                rank += 1

            # The question ! When synchronize couchdb views ?
            self.with_fields.sync(database)
            self.by_id.sync(database)

    def find(self, database, id=False, fields=False):
        document = None
        options  = {}
        if id:
            if fields:  options = { 'startkey' : [id], 'endkey' : [id, {}] }
            else:       options = { 'key' : [id, 0] }

        for row in self.with_fields(database, **options):
            if row.value['metatype'] in ('DataType'):
                if document:
                    yield document

                document = DataType.wrap(row.value)

            elif 'DataTypeField' in row.value['metatype']:
                document.fields.append(globals()[row.value['metatype']].wrap(row.value))

        if document:
            yield document

    def build(self, database, values):
        model_document = LegoDocument(self.id)
        for field in self.fields:
            if field.id in values.keys():
                model_document._data[field.id] = values[field.id]

        model_document.store(database)
        

class DataTypeField(MetaLegoDocument):
    """
    Field of a database document type.
    """

    datatype = TextField()
    rank     = IntegerField()
    #default  = None

    def __init__(self, label=None, default=None):
        super(DataTypeField, self).__init__()

        if label:   self.label = label
        if default: self.default = default


class AdressDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        super(AdressDataTypeField, self).__init__(label=label, default=default)


class StringDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        super(StringDataTypeField, self).__init__(label=label, default=default)


class FloatDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        super(FloatDataTypeField, self).__init__(label=label, default=default)


class IntegerDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        super(IntegerDataTypeField, self).__init__(label=label, default=default)


class RelationDataTypeField(DataTypeField):

    relation = TextField()

    def __init__(self, label=None, relation=None):
        super(RelationDataTypeField, self).__init__(label=label)
        if relation:
            self.relation = relation

