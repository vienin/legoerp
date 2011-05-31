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

from model.datatype import DataType
from model.perspective import Perspective
from model.operation import Operation
from model.couch import LegoDocument


# TODO: Move this from here
couchdb = Server()
try:
    database = couchdb['lego_erp_test']
except:
    database = couchdb.create('lego_erp_test')

if not len(couchdb['lego_erp_test']):
    from model import load_model
    from examples import simplecrm

    load_model(database, simplecrm.model)


def index(request):
    '''
    index.html display the view list and each view operations.
    '''

    # Get all perspectives
    perspectives = {}
    for view in Perspective().list(database):
        perspectives[view.id] = view

    return render_to_response('explorer/index.html', { 'perspectives' : perspectives })

def operation(request, viewid, id):
    '''
    operation.html display an operation form.
    '''

    perspective = Perspective().find(database, viewid)
    operation   = Operation().find(database, id)

    # If the form has been submitted...
    if request.method == 'POST':
        form = operation.form(post=request.POST)
        if form.is_valid():

            operation.datatype.build(database, form.cleaned_data)
            return HttpResponseRedirect('/perspective/%s' % viewid)
    else:
        form = operation.form()

    return render_to_response('explorer/operation.html', { 'form' : form,
                                                           'perspective' : perspective,
                                                           'operation'   : operation })

def perspective(request, id):
    '''
    perspective.html display a perspective of a datatype.
    '''

    perspective = Perspective().find(database, id)

    contents = []
    for content in LegoDocument().contents(database, perspective.datatype.id):
        values = []
        for field in perspective.datafields:
            values.append(content._data.get(field.id))
        values.append(content.id)
        contents.append(values)

    return render_to_response('explorer/perspective.html', { 'perspective' : perspective,
                                                             'contents'    : contents })

def datatype(request, viewid, id, operationid=False):
    '''
    dataype.html display fields and values of a DataType instance (content).
    '''

    perspective = Perspective().find(database, viewid)
    datatype    = DataType().find(database, perspective.datatype.id)

    content = LegoDocument().content(database, datatype.id, id)

    form = None
    operation = None
    if operationid: 
        operation = Operation().find(database, operationid)

        # If the form has been submitted...
        if request.method == 'POST':
            form = operation.form(post=request.POST)

            if form.is_valid():
                for field in datatype.fields:
                    if field.id in form.cleaned_data.keys():
                        content._data[field.id] = form.cleaned_data[field.id]

                database.save(content._data)
    
                return HttpResponseRedirect('/datatype/%s/%s' % (perspective.id, content.id))

        # Build the form corresponding to the current operation
        else:
            form = operation.form(content=content)

    # Build a non editable form to display the values of the content fields
    else:
        form = Operation().form(fields=datatype.fields)

    return render_to_response('explorer/datatype.html', { 'perspective' : perspective,
                                                          'operation'   : operation,
                                                          'datatype'    : datatype,
                                                          'content'     : content,
                                                          'form'        : form })
