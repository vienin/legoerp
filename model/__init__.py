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
# File: model.py

from datatype import DataType, DataTypeFieldAdress, DataTypeFieldString
from datatype import DataTypeFieldFloat, DataTypeFieldInteger, DataTypeFieldRelation
from model.perspective import Perspective
from model.operation import Operation, AddDataOperation, DelDataOperation, UpdateDataOperation


ordered_types = [ DataTypeFieldAdress,
                  DataTypeFieldString,
                  DataTypeFieldFloat,
                  DataTypeFieldInteger,
                  DataTypeFieldRelation,
                  DataType,
                  AddDataOperation,
                  DelDataOperation,
                  UpdateDataOperation,
                  Perspective ]

def replace_tuple_by_object(model, item):
    if isinstance(item, tuple):
        meta, key = item
        return model[meta][key]

    else:
        return item

def load_model(database, model):
    for metatype in ordered_types: #model:
        for document in model[metatype]:
            for field in model[metatype][document]:
                # If field is a metatype reference,
                # replace the tuple by the metatype instance.
                if not isinstance(model[metatype][document][field], list):
                    model[metatype][document][field] = \
                        replace_tuple_by_object(model, model[metatype][document][field])

                else:
                    for item in model[metatype][document][field]:
                        model[metatype][document][field][model[metatype][document][field].index(item)] = \
                            replace_tuple_by_object(model, item)

            # Replace the model dictionary by the created database document
            model[metatype][document] = metatype(database=database, **model[metatype][document])
