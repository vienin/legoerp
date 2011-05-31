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

from couch import MetaLegoDocument, LegoDocument, TextField


class DataTypeField(MetaLegoDocument):
    """
    Field of a database document type.
    """

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeField, self).__init__(database=database,
                                            label=label,
                                            **kwords)


class DataTypeFieldAdress(DataTypeField):

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeFieldAdress, self).__init__(database=database,
                                                  label=label,
                                                  **kwords)


class DataTypeFieldString(DataTypeField):

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeFieldString, self).__init__(database=database,
                                                  label=label,
                                                  **kwords)


class DataTypeFieldFloat(DataTypeField):

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeFieldFloat, self).__init__(database=database,
                                                 label=label,
                                                 **kwords)


class DataTypeFieldInteger(DataTypeField):

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeFieldInteger, self).__init__(database=database,
                                                   label=label,
                                                   **kwords)


class DataTypeFieldRelation(DataTypeField):

    relation = TextField()

    def __init__(self, database=None, label=None, **kwords):
        super(DataTypeFieldRelation, self).__init__(database=database,
                                                    label=label,
                                                    **kwords)


class DataType(MetaLegoDocument):
    """
    Description of a database document type.
    """

    __decls__ = { 'DataTypeFieldAdress'   : DataTypeFieldAdress,
                  'DataTypeFieldString'   : DataTypeFieldString,
                  'DataTypeFieldFloat'    : DataTypeFieldFloat,
                  'DataTypeFieldInteger'  : DataTypeFieldInteger,
                  'DataTypeFieldRelation' : DataTypeFieldRelation }

    fields = []

    def __init__(self, database=None, label=None, **kwords):
        super(DataType, self).__init__(database=database,
                                       label=label,
                                       **kwords)

    def build(self, database, values):
        content = LegoDocument(self.id)
        for fieldid in values:
            content._data[fieldid] = values[fieldid]

        content.store(database)
