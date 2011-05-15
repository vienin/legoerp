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
from metamodel.datatype import DataType, DataTypeForm
from metamodel.operation import Operation

from metamodel.couch import LegoDocument

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
    index.html display the view list and each view operations.
    '''

    # Get all views
    displayed_views = View().find(database)

    # Get all operations indexed by view
    operations = {}
    for operation in Operation().find_by_view(database):
        
        # Arg...
        for fullop in operation.find(database, label=operation.label, steps=True):
            if fullop.at_list_level():
                if not operations.has_key(operation.view):
                    operations[operation.view] = []

                    operations[operation.view].append(operation)

    return render_to_response('model_explorer/index.html', { 'views' : displayed_views,
                                                             'operations' : operations })

def operation(request, id):
    '''
    operation.html display an operation form.
    '''

    operation = Operation().find_by_id(database, id)
    
    fullop = None
    for first in Operation().find(database, label=operation.label, steps=True):
        fullop = first
        break

    viewid = None
    datatype = None
    for first in View().find(database, label=operation.view):
        datatype = first.datatype
        viewid = first.id
        break
    
    for first in DataType().find(database, label=datatype, fields=True):
        datatype = first
        break

    if request.method == 'POST': # If the form has been submitted...
        form = DataTypeForm(request.POST, datatype=datatype)
        if form.is_valid(): # All validation rules pass
            
            datatype.build(database, form.cleaned_data)
            return HttpResponseRedirect('/view/%s' % viewid)
    else:
        form = DataTypeForm(datatype=datatype)

    return render_to_response('model_explorer/operation.html', { 'form': form,
                                                                 'viewid' : viewid,
                                                                 'operation' : fullop,
                                                                 'datatype'  : datatype })

def view(request, id):
    '''
    view.html display a view of a datatype.
    '''

    view = View().find_by_id(database, id)

    datatype = None
    for first in DataType().find(database, label=view.datatype, fields=True):
        datatype = first
        break

    contents = []
    for content in LegoDocument().contents(database, datatype.label):
        values = []
        for field in datatype.fields:
            values.append(content._data.get(field.label))
        values.append(content.id)
        contents.append(values)

    # Get the view operations
    operations = []
    for operation in Operation().find_by_view(database, view=view.label):
        # Arg...
        for fullop in operation.find(database, label=operation.label, steps=True):
            if fullop.at_list_level():
                operations.append(operation)

    return render_to_response('model_explorer/view.html', { 'view' : view,
                                                            'datatype' : datatype,
                                                            'contents' : contents,
                                                            'operations' : operations })

def datatype(request, viewid, id, operationid=False):
    '''
    dataype.html display fields and values of a DataTypeInstance.
    '''

    view = View().find_by_id(database, viewid)

    fulltype = None
    for first in DataType().find(database, label=view.datatype, fields=True):
        fulltype = first
        break

    values = []
    model_doc = None
    for content in LegoDocument().contents(database, fulltype.label, id):
        for field in fulltype.fields:
            values.append(content._data.get(field.label))
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
                    model_doc._data[field.label] = form.cleaned_data[field.id]

            database.save(model_doc._data)

            return HttpResponseRedirect('/datatype/%s/%s' % (view.id, model_doc.id))
    else:
        form = DataTypeForm(datatype=fulltype, initial=content._data)

    # Get the view operations
    operations = Operation().find_by_view(database, view=view.label)

    return render_to_response('model_explorer/datatype.html', { 'cid'      : content.id,
                                                                'viewid'   : viewid,
                                                                'datatype' : fulltype,
                                                                'operations' : operations,
                                                                'form'     : form,
                                                                'edit'     : edit,
                                                                'values'   : values})
