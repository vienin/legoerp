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
# file: views.py

from django.http import Http404,HttpResponseRedirect
from django.shortcuts import render_to_response

from couchdb.client import Server

from metamodel.view import View
from metamodel.datatype import DataType
from metamodel.operation import Operation


# TODO: Move this from here
couchdb = Server()
try:
    database = couchdb['lego_erp_test']
except:
    database = couchdb.create('lego_erp_test')
    
    from metamodel.load import load_model
    from examples import simplecrm

    load_model(database, simplecrm.model)


def index(request):
    '''
    Index.html display the view list and each view operations.
    '''

    # Get all views
    displayed_views = View().find(database)

    # Get all operations indexed by view
    operations = {}
    for operation in Operation().find_by_view(database):
        if not operations.has_key(operation.view):
            operations[operation.view] = []

        operations[operation.view].append(operation)

    return render_to_response('model_explorer/index.html', { 'views' : displayed_views,
                                                             'operations' : operations })
