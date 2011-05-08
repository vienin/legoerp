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
# File: view.py

from couch import *


class View(LegoDocument):
    """
    Description of a view database contents.
    """

    datatype = TextField()
    #datafields = {}

    by_label = ViewField(design='view',
                         map_fun='''\
                   function(doc) {
                       if (doc.type == 'View') {
                           emit(doc.label, doc);
                       }
                   }''')

    def __init__(self, database=None, label=None, datatype=None):
        LegoDocument.__init__(self)
        
        if database:
            self.label    = label
            self.datatype = datatype
            self.store(database)

            self.by_label.sync(database)

    def find(self, database, label=False):
        document = None
        options  = {}
        
        if label:
            options = { 'key' : label }

        for doc in self.by_label(database, **options):
            if doc.type in ('View'):
                yield doc
