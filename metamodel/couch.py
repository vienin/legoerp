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

from couchdb.mapping import *


class MetaLegoDocument(Document):

    metatype = TextField()
    label    = TextField()

    by_id = ViewField(design='datatype',
                         map_fun='''\
                   function(doc) {
                       emit(doc._id, doc);
                   }''')

    def __init__(self):
        Document.__init__(self)
        self.metatype = self.__class__.__name__

    def __repr__(self):
        return self.label.encode('utf-8')

    def find_by_id(self, database, id):
        document = None
        for doc in self.by_id(database, key=id):
            document = doc
            break
        return document

class LegoDocument(Document):

    type = TextField()

    by_type = ViewField(design='contents',
                        map_fun='''\
                   function(doc) {
                       if (doc.type) {
                           emit([doc.type, doc._id], doc);
                       }
                   }''')

    def __init__(self, type=None):
        Document.__init__(self)

        self.type = type

    def __repr__(self):
        return self.type.encode('utf-8')

    def contents(self, database, type, id=None):
        self.by_type.sync(database)

        if id:  options = { 'key' : [type, id] }
        else:   options = { 'startkey' : [type], 'endkey' : [type, {}] }

        for content in self.by_type(database, **options):
            yield content
