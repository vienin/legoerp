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
# File: simplecrm.py

from couchdb.client import Server
from metamodel.datatype import *
from metamodel.view import View
from metamodel.operation import *


model = [ { 'type'   : DataType,
            'label'  : u'Produit',
            'fields' : [ StringDataTypeField(u'Nom'),
                         FloatDataTypeField(u'Prix unitaire'),
                         IntegerDataTypeField(u'Quantitée disponible'),
                         FloatDataTypeField(u'Dégagement Co2 (mlg)'), ],
          },

          { 'type'   : DataType,
            'label'  : u'Client',
            'fields' : [ StringDataTypeField(u'Prénom'),
                         StringDataTypeField(u'Nom'),
                         AdressDataTypeField(u'Adresse'), ],
          },

          { 'type'   : DataType,
            'label'  : u'Commande',
            'fields' : [ StringDataTypeField(u'Numéro'),
                         RelationDataTypeField(u'Produit acheté', u'Produit'),
                         RelationDataTypeField(u'Client concerné', u'Client'),
                         IntegerDataTypeField(u'Quantitée'), ],
          },

          { 'type'     : View,
            'label'    : u'Produits',
            'datatype' : u'Produit',
          },

          { 'type'  : Operation,
            'label' : u'Ajouter produit',
            'view'  : u'Produits',
            'steps' : [ AddDataOperationStep(u'Ajouter produit step 1'), ],
          }
        ]
