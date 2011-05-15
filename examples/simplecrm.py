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


model = [ { 'metatype' : DataType,
            'label'    : u'Produit',
            'fields'   : [ StringDataTypeField(u'Nom'),
                         FloatDataTypeField(u'Prix unitaire'),
                         IntegerDataTypeField(u'Quantitée disponible'),
                         FloatDataTypeField(u'Dégagement Co2 (mlg)'), ],
          },

          { 'metatype' : DataType,
            'label'    : u'Client',
            'fields'   : [ StringDataTypeField(u'Prénom'),
                           StringDataTypeField(u'Nom'),
                           AdressDataTypeField(u'Adresse'), ],
          },

          { 'metatype' : DataType,
            'label'    : u'Commande',
            'fields'   : [ StringDataTypeField(u'Numéro'),
                           RelationDataTypeField(u'Produit acheté', u'Produit'),
                           RelationDataTypeField(u'Client concerné', u'Client'),
                           IntegerDataTypeField(u'Quantitée'), ],
          },

          { 'metatype' : DataType,
            'label'    : u'Frais',
            'fields'   : [ StringDataTypeField(u'Titre'),
                           FloatDataTypeField(u'Montant'), ],
          },

          { 'metatype' : View,
            'label'    : u'Liste des produits',
            'datatype' : u'Produit',
          },

          { 'metatype' : View,
            'label'    : u'Liste des clients',
            'datatype' : u'Client',
          },

          { 'metatype' : View,
            'label'    : u'Liste des commandes',
            'datatype' : u'Commande',
          },

          { 'metatype' : View,
            'label'    : u'Chiffre d\'affaires',
            'datatype' : u'Frais',
          },

          { 'metatype' : View,
            'label'    : u'Statistiques',
            'datatype' : u'Frais',
          },

          { 'metatype' : View,
            'label'    : u'Matériel et notes de frais',
            'datatype' : u'Frais',
          },

          { 'metatype' : Operation,
            'label'    : u'Approvisionnement',
            'view'     : u'Liste des produits',
            'steps'    : [ AddDataOperationStep(u'Approvisionnement step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Mettre à jour un produit',
            'view'     : u'Liste des produits',
            'steps'    : [ UpdateDataOperationStep(u'Mettre à jour un produit step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Nouveau client',
            'view'     : u'Liste des clients',
            'steps'    : [ AddDataOperationStep(u'Nouveau client step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Mettre à jour client',
            'view'     : u'Liste des clients',
            'steps'    : [ UpdateDataOperationStep(u'Mettre à jour client'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Nouvelle commande',
            'view'     : u'Liste des commandes',
            'steps'    : [ AddDataOperationStep(u'Nouvelle commande step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Annuler commande',
            'view'     : u'Liste des commandes',
            'steps'    : [ DelDataOperationStep(u'Annuler commande step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Achat de matériel',
            'view'     : u'Matériel et notes de frais',
            'steps'    : [ AddDataOperationStep(u'Achat de matériel step 1'), ],
          },

          { 'metatype' : Operation,
            'label'    : u'Saisir note de frais',
            'view'     : u'Matériel et notes de frais',
            'steps'    : [ AddDataOperationStep(u'Saisir note de frais step 1'), ],
          },

        ]
