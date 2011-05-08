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

from couch import *


class Operation(LegoDocument):
    """
    Description of an operation on the database.
    Typically, an operation is a set of updates
    on a single or a set of database documents.
	"""

    view = TextField()

    by_view  = ViewField(design='operation',
                         map_fun='''\
                   function(doc) {
                       if (doc.type == 'Operation') {
                           emit(doc.view, doc);
                       }
                   }''')

    by_label = ViewField(design='operation',
                         wrapper=None,
                         map_fun='''\
                   function(doc) {
                       if (doc.type == 'Operation') {
                           emit([doc.label, 0], doc);
                       } else if (doc.type.indexOf('OperationStep') > -1) {
                           emit([doc.operation, doc.rank], doc);
                       }
                   }''')

    steps = None

    def __init__(self, database=None, label=None, view=None, steps=[]):
        LegoDocument.__init__(self)

        self.steps = []
        if database:
            self.label = label
            self.view = view
            self.store(database)

            rank = 1
            for step in steps:
                step.rank = rank
                step.operation = self.label
                step.store(database)
                self.steps.append(step)
                rank += 1
            
            self.by_label.sync(database)
            self.by_view.sync(database)

    def find(self, database, label=False, steps=False):
        document = None
        options  = {}
        if label:
            if steps:   options = { 'startkey' : [label], 'endkey' : [label, {}] }
            else:       options = { 'key' : [label, 0] }

        for row in self.by_label(database, **options):
            if row.value['type'] in ('Operation'):
                if document:
                    yield document

                document = DataType.wrap(row.value)

            elif 'OperationStep' in row.value['type']:
                document.steps.append(globals()[row.value['type']].wrap(row.value))

        if document:
            yield document

    def find_by_view(self, database, view=False):
        options  = {}
        if view:
            options = { 'key' : view }

        for doc in self.by_view(database, **options):
            yield doc

class OperationStep(LegoDocument):
    """
    Single update on databse documents.
    """

    operation = TextField()
    rank      = IntegerField()

    def __init__(self, label=None):
        LegoDocument.__init__(self)

        if label:   self.label = label


class UpdateDataOperationStep(OperationStep):
    fields = {}
    values = {}

    def __init__(self, label=None, fields=False, values=False):
        OperationStep.__init__(self, label)
        self.fields = fields
        self.values = values

        
class AddDataOperationStep(OperationStep):

    def __init__(self, label=None):
        OperationStep.__init__(self, label)

        
class DelDataOperationStep(OperationStep):

    def __init__(self, label=None):
        OperationStep.__init__(self, label)
