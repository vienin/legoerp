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

from model.datatype import *
from model.view import View
from model.operation import *


model = { DataType : { 'product' : { 'label'    : u'Produit',
                                     'fields'   : [ StringDataTypeField(u'Nom'),
                                                  FloatDataTypeField(u'Prix unitaire'),
                                                  IntegerDataTypeField(u'Quantitée disponible'),
                                                  FloatDataTypeField(u'Dégagement Co2 (mlg)'), ],
                                   },

                        'client' : { 'label'    : u'Client',
                                     'fields'   : [ StringDataTypeField(u'Prénom'),
                                                    StringDataTypeField(u'Nom'),
                                                    AdressDataTypeField(u'Adresse'), ],
                                   },

                        'order'  : { 'label'    : u'Commande',
                                     'fields'   : [ StringDataTypeField(u'Numéro'),
                                                    RelationDataTypeField(u'Produit acheté', u'Produit'),
                                                    RelationDataTypeField(u'Client concerné', u'Client'),
                                                    IntegerDataTypeField(u'Quantitée'), ],
                                   },

                        'cost'   : { 'label'    : u'Frais',
                                     'fields'   : [ StringDataTypeField(u'Titre'),
                                                    FloatDataTypeField(u'Montant'), ],
                                   },
                     },

          View : { 'products' : { 'label'    : u'Liste des produits',
                                  'datatype' : (DataType, 'product'),
                                },

                   'clients'  : { 'label'    : u'Liste des clients',
                                  'datatype' : (DataType, 'client'),
                                },

                   'orders'   : { 'label'    : u'Liste des commandes',
                                  'datatype' : (DataType, 'order'),
                                },

                   'costs'    : { 'label'    : u'Chiffre d\'affaires',
                                  'datatype' : (DataType, 'cost'),
                                },

                   'stats'    : { 'label'    : u'Statistiques',
                                  'datatype' : (DataType, 'cost'),
                                },

                   'buy'      : { 'label'    : u'Matériel et notes de frais',
                                  'datatype' : (DataType, 'cost'),
                                },
                 },

            Operation : { 'operation_0' : { 'label' : u'Approvisionnement',
                                            'view'  : (View, 'products'),
                                            'steps' : [ AddDataOperationStep(), ],
                                          },

                          'operation_1' : { 'label' : u'Mettre à jour un produit',
                                            'view'  : (View, 'products'),
                                            'steps' : [ UpdateDataOperationStep(), ],
                                          },

                          'operation_2' : { 'label' : u'Nouveau client',
                                            'view'  : (View, 'clients'),
                                            'steps' : [ AddDataOperationStep(), ],
                                          },

                          'operation_3' : { 'label' : u'Mettre à jour client',
                                            'view'  : (View, 'clients'),
                                            'steps' : [ UpdateDataOperationStep(), ],
                                          },

                          'operation_4' : { 'label' : u'Nouvelle commande',
                                            'view'  : (View, 'orders'),
                                            'steps' : [ AddDataOperationStep(), ],
                                          },

                          'operation_5' : { 'label' : u'Annuler commande',
                                            'view'  : (View, 'orders'),
                                            'steps' : [ DelDataOperationStep(), ],
                                          },

                          'operation_6' : { 'label' : u'Achat de matériel',
                                            'view'  : (View, 'costs'),
                                            'steps' : [ AddDataOperationStep(), ],
                                          },

                          'operation_7' : { 'label' : u'Saisir note de frais',
                                            'view'  : (View, 'costs'),
                                            'steps' : [ AddDataOperationStep(), ],
                                          },
                        }
        }
