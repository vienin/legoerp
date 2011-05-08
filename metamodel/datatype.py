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


class DataType(LegoDocument):
    """
    Description of a database document type.
    """

    by_label = ViewField(design='datatype',
                         wrapper=None,
                         map_fun='''\
                   function(doc) {
                       if (doc.type == 'DataType') {
                           emit([doc.label, 0], doc);
                       } else if (doc.type.indexOf('DataTypeField') > -1) {
                           emit([doc.datatype, doc.rank], doc);
                       }
                   }''')

    fields = None

    def __init__(self, database=None, label=None, fields=[]):
        LegoDocument.__init__(self)

        self.fields = []
        if database:
            self.label = label
            self.store(database)

            rank = 1
            for field in fields:
                field.rank = rank
                field.datatype = self.label
                field.store(database)
                self.fields.append(field)
                rank += 1
            
            self.by_label.sync(database)

    def find(self, database, label=False, fields=False):
        document = None
        options  = {}
        if label:
            if fields:  options = { 'startkey' : [label], 'endkey' : [label, {}] }
            else:       options = { 'key' : [label, 0] }

        for row in self.by_label(database, **options):
            if row.value['type'] in ('DataType'):
                if document:
                    yield document

                document = DataType.wrap(row.value)

            elif 'DataTypeField' in row.value['type']:
                document.fields.append(globals()[row.value['type']].wrap(row.value))

        if document:
            yield document

class DataTypeField(LegoDocument):
    """
    Field of a database document type.
    """

    datatype = TextField()
    rank     = IntegerField()
    #default  = None

    def __init__(self, label=None, default=None):
        LegoDocument.__init__(self)

        if label:   self.label = label
        if default: self.default = default


class AdressDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        DataTypeField.__init__(self, label, default)


class StringDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        DataTypeField.__init__(self, label, default)


class FloatDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        DataTypeField.__init__(self, label, default)


class IntegerDataTypeField(DataTypeField):

    def __init__(self, label=None, default=None):
        DataTypeField.__init__(self, label, default)


class RelationDataTypeField(DataTypeField):

    relation = TextField()

    def __init__(self, label=None, relation=None):
        DataTypeField.__init__(self, label)
        if relation:
            self.relation = relation

