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


class OneToOneField(Field):

    metatype = None

    def __init__(self, metatype):
        self.metatype = metatype


class OneToManyField(Field):

    metatype = None

    def __init__(self, metatype):
        self.metatype = metatype


class MetaLegoDocument(Document):

    __decls__ = {}

    metatype = TextField()
    label    = TextField()

    referenced_in = DictField()

    by_metatype = ViewField(design='meta',
                            wrapper=None,
                            map_fun='''\
                    function(doc) {
                        if (doc.metatype) {
                            emit([doc.metatype, doc._id, null], doc);
                            
                            // Max iterations is the amount of classes that inherit
                            // from MetaLegoDocument within the metamodel (Beware to maintain < 10).
                            for(var referencer_type in doc.referenced_in) {
                            
                                // Max iteration is the maximum amount of attributes
                                // related to separate documents in a class that inherit
                                // from MetaLogoDocument within the metamodel (Beware to maintain < 10).
                                for(var attr in doc.referenced_in[referencer_type]) {
                                
                                    // Max iterations increase with the amount of
                                    // DataType instances defined by the user.
                                    for(var ref = 0; ref < doc.referenced_in[referencer_type][attr].length; ref++) {
                                        emit([referencer_type, doc.referenced_in[referencer_type][attr][ref], attr], doc);
                                    }
                                }
                            }
                        }
                    }''')

    by_id = ViewField(design='meta',
                      wrapper=None,
                      map_fun='''\
                    function(doc) {
                        if (doc.metatype) {
                            emit([doc._id, null, doc.metatype], doc);

                            // Max iterations is the amount of classes that inherit
                            // from MetaLegoDocument within the metamodel (Beware to maintain < 10).
                            for(var referencer_type in doc.referenced_in) {
                            
                                // Max iteration is the maximum amount of attributes
                                // related to separate documents in a class that inherit
                                // from MetaLogoDocument within the metamodel (Beware to maintain < 10).
                                for(var attr in doc.referenced_in[referencer_type]) {
                                
                                    // Max iterations increase with the amount of
                                    // DataType instances defined by the user.
                                    for(var ref = 0; ref < doc.referenced_in[referencer_type][attr].length; ref++) {
                                        emit([doc.referenced_in[referencer_type][attr][ref], attr, doc.metatype], doc);
                                    }
                                }
                            }
                        }
                   }''')

    def __init__(self, database=None, label=None, **kwords):
        Document.__init__(self)
        self.metatype = self.__class__.__name__

        if label:
            self.label = label

        if database:
            attrs = kwords.keys()
            for attr in attrs:
                try:
                    # Test the attr
                    getattr(self, attr)

                    # kword is a document field value, set the document field to the value. 
                    if self._data.has_key(attr):
                        setattr(self, attr, kwords[attr])
                        del kwords[attr]

                except AttributeError, e:
                    # Loaded model do not match to metamodel
                    raise

            # Create the current document
            self.store(database)

            for attr in kwords:
                # kword is a separate document, create/update the separate document,
                # and add the current document id to its refenreced_in list.
                if isinstance(getattr(self, attr), list):
                    setattr(self, attr, [])
                if not isinstance(kwords[attr], list):
                    kwords[attr] = [ kwords[attr] ]

                for document in kwords[attr]:
                    if not document.referenced_in.has_key(self.metatype):
                        document.referenced_in[self.metatype] = {}
                    if not document.referenced_in[self.metatype].has_key(attr):
                        document.referenced_in[self.metatype][attr] = []

                    document.referenced_in[self.metatype][attr].append(self.id)

                    #document.rank = rank
                    document.store(database)
                    if isinstance(getattr(self, attr), list):
                        getattr(self, attr).append(document)

                    else:
                        setattr(self, attr, document)

            # Synchronize the views here for instance..
            self.by_id.sync(database)
            self.by_metatype.sync(database)

    def __repr__(self):
        return self.label.encode('utf-8')

    def list(self, database):
        document = None
        options = { 'startkey' : [self.metatype], 'endkey' : [self.metatype, {}] }

        for row in self.by_metatype(database, **options):
            key, id, attr = row.key
            metatype = row.value['metatype']

            # Build the requested object identified by 'id'
            if not attr:
                if document:
                    yield document

                document = self.__class__.wrap(row.value)

            # Build objects from separate documents, and fill
            # the list of attr that are related to.
            else:
                separate_doc = self.__decls__[metatype].wrap(row.value)

                if isinstance(getattr(document, attr), list):
                    if not getattr(document, attr):
                        setattr(document, attr, [])
                    getattr(document, attr).append(separate_doc)
                
                else:
                    setattr(document, attr, separate_doc)
            
        if document:
            yield document

    def find(self, database, id):
        document = None
        options = { 'startkey' : [id], 'endkey' : [id, {}] }

        for row in self.by_id(database, **options):
            print row.key
            id, attr, metatype = row.key

            # Build the requested object identified by 'id'
            if not attr:
                if self.__class__.__name__ == metatype:
                    document = self.__class__.wrap(row.value)
                else:
                    document = self.__decls__[metatype].wrap(row.value)

            # Build objects from separate documents, and fill
            # the list that are related to.
            else:
                separate_doc = self.__decls__[metatype].wrap(row.value)

                if isinstance(getattr(document, attr), list):
                    if not getattr(document, attr):
                        setattr(document, attr, [])
                    getattr(document, attr).append(separate_doc)
                
                else:
                    setattr(document, attr, separate_doc)
            
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

    def get(self, name):
        return Document.get(self, name, None)

    def content(self, database, type, id):
        for content in self.contents(database, type, id):
            return content

    def contents(self, database, type, id=None):
        self.by_type.sync(database)

        if id:  options = { 'key' : [type, id] }
        else:   options = { 'startkey' : [type], 'endkey' : [type, {}] }

        for content in self.by_type(database, **options):
            yield content
