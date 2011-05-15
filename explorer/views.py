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

from model.view import View
from model.datatype import DataType, DataTypeForm
from model.operation import Operation

from model.couch import LegoDocument

# TODO: Move this from here
couchdb = Server()
try:
    database = couchdb['lego_erp_test']
except:
    database = couchdb.create('lego_erp_test')

if not len(couchdb['lego_erp_test']):
    from model.load import load_model
    from examples import simplecrm

    load_model(database, simplecrm.model)


def index(request):
    '''
    index.html display the view list and each view operations.
    '''

    # Get all views
    displayed_views = {}
    for view in View().find(database):
        displayed_views[view.id] = view

    # Get all operations indexed by view
    operations = {}
    for operation in Operation().find_by_view(database):
        if not operations.has_key(operation.view):
            operations[operation.view] = []
            
        # Arg...
        for fullop in operation.find(database, id=operation.id, steps=True):
            if fullop.at_list_level():
                operations[operation.view].append(operation)

    return render_to_response('explorer/index.html', { 'views'      : displayed_views,
                                                       'operations' : operations })

def operation(request, id):
    '''
    operation.html display an operation form.
    '''

    operation = Operation().find_by_id(database, id)
    
    fullop = None
    for first in Operation().find(database, id=operation.id, steps=True):
        fullop = first
        break

    viewid = None
    datatype = None
    for first in View().find(database, id=operation.view):
        datatype = first.datatype
        viewid = first.id
        break
    
    for first in DataType().find(database, id=datatype, fields=True):
        datatype = first
        break

    if request.method == 'POST': # If the form has been submitted...
        form = DataTypeForm(request.POST, datatype=datatype)
        if form.is_valid(): # All validation rules pass
            
            datatype.build(database, form.cleaned_data)
            return HttpResponseRedirect('/view/%s' % viewid)
    else:
        form = DataTypeForm(datatype=datatype)

    return render_to_response('explorer/operation.html', { 'form'      : form,
                                                           'viewid'    : viewid,
                                                           'operation' : fullop,
                                                           'datatype'  : datatype })

def view(request, id):
    '''
    view.html display a view of a datatype.
    '''

    view = View().find_by_id(database, id)

    datatype = None
    for first in DataType().find(database, id=view.datatype, fields=True):
        datatype = first
        break

    contents = []
    for content in LegoDocument().contents(database, datatype.id):
        values = []
        for field in datatype.fields:
            values.append(content._data.get(field.id))
        values.append(content.id)
        contents.append(values)

    # Get the view operations
    operations = []
    for operation in Operation().find_by_view(database, view=view.id):
        # Arg...
        for fullop in operation.find(database, id=operation.id, steps=True):
            if fullop.at_list_level():
                operations.append(operation)

    return render_to_response('explorer/view.html', { 'view'       : view,
                                                      'datatype'   : datatype,
                                                      'contents'   : contents,
                                                      'operations' : operations })

def datatype(request, viewid, id, operationid=False):
    '''
    dataype.html display fields and values of a DataTypeInstance.
    '''

    view = View().find_by_id(database, viewid)

    fulltype = None
    for first in DataType().find(database, id=view.datatype, fields=True):
        fulltype = first
        break

    values = []
    model_doc = None
    for content in LegoDocument().contents(database, fulltype.id, id):
        for field in fulltype.fields:
            values.append(content._data.get(field.id))
        model_doc = content
        break

    edit = False
    if operationid:
        edit = True

    if request.method == 'POST': # If the form has been submitted...
        form = DataTypeForm(request.POST, datatype=fulltype)
        if form.is_valid(): # All validation rules pass
            for field in fulltype.fields:
                if field.id in form.cleaned_data.keys():
                    model_doc._data[field.id] = form.cleaned_data[field.id]

            database.save(model_doc._data)

            return HttpResponseRedirect('/datatype/%s/%s' % (view.id, model_doc.id))
    else:
        form = DataTypeForm(datatype=fulltype, initial=content._data)

    # Get the view operations
    operations = Operation().find_by_view(database, view=view.id)

    return render_to_response('explorer/datatype.html', { 'cid'        : content.id,
                                                          'viewid'     : viewid,
                                                          'datatype'   : fulltype,
                                                          'operations' : operations,
                                                          'form'       : form,
                                                          'edit'       : edit,
                                                          'values'     : values})
