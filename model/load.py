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
# File: load.py

from model.datatype import DataType
from model.view import View
from model.operation import Operation


def load_model(database, model):
    for metatype in [ DataType, View, Operation ]: #model:
        for document in model[metatype]:
            for field in model[metatype][document]:
                # If field is a metatype reference,
                # replace the tuple by the metatype instance id.
                #print "-- > " + str(model[metatype][document][field])
                if isinstance(model[metatype][document][field], tuple):
                    type, key = model[metatype][document][field]
                    model[metatype][document][field] = model[type][key].id

            # Replace the model dictionary by the created database document
            model[metatype][document] = metatype(database=database,
                                                 **model[metatype][document])
