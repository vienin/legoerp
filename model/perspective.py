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
# File: perspective.py

from couch import MetaLegoDocument, TextField

from datatype import DataType, DataTypeFieldAdress, DataTypeFieldString
from datatype import DataTypeFieldFloat, DataTypeFieldInteger, DataTypeFieldRelation
from operation import UpdateDataOperation, AddDataOperation, DelDataOperation


class Perspective(MetaLegoDocument):
    """
    Description of a view database contents.
    """

    __decls__ = { 'DataType'              : DataType,
                  'UpdateDataOperation'   : UpdateDataOperation,
                  'AddDataOperation'      : AddDataOperation,
                  'DelDataOperation'      : DelDataOperation,
                  'DataTypeFieldAdress'   : DataTypeFieldAdress,
                  'DataTypeFieldString'   : DataTypeFieldString,
                  'DataTypeFieldFloat'    : DataTypeFieldFloat,
                  'DataTypeFieldInteger'  : DataTypeFieldInteger,
                  'DataTypeFieldRelation' : DataTypeFieldRelation }

    datatype   = None
    operations = []
    datafields = []

    def __init__(self, database=None, label=None, **kwords):
        super(Perspective, self).__init__(database, label, **kwords)
