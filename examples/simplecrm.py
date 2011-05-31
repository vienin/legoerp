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
from model.perspective import Perspective
from model.operation import *


model = { DataTypeFieldString : { 'product_name' : { 'label' : u'Nom', },
                                  'client_first' : { 'label' : u'Prénom', },
                                  'client_last'  : { 'label' : u'Nom', },
                                  'order_number' : { 'label' : u'Numéro', },
                                  'cost_title'   : { 'label' : u'Titre', },
                                },

          DataTypeFieldInteger : { 'product_quan' : { 'label' : u'Quantitée disponible', },
                                   'order_quanti' : { 'label' : u'Quantitée', },
                                 },

          DataTypeFieldFloat : { 'product_co2' : { 'label' : u'Dégagement Co2 (mlg)', },
                                 'product_pri' : { 'label' : u'Prix unitaire', },
                                 'cost_price'  : { 'label' : u'Montant', },
                               },

          DataTypeFieldAdress : { 'client_addr' : { 'label' : u'Adresse', }, },
          
          DataTypeFieldRelation : { 'order_product' : { 'label'        : u'Produit acheté',
                                                        'relationship' : u'Produit' },
                                    'order_client'  : { 'label'        : u'Client concerné',
                                                        'relationship' : u'Client' },
                                  },

          DataType : { 'product' : { 'label'    : u'Produit',
                                     'fields'   : [ (DataTypeFieldString, 'product_name'),
                                                    (DataTypeFieldFloat, 'product_pri'),
                                                    (DataTypeFieldInteger, 'product_quan'),
                                                    (DataTypeFieldFloat, 'product_co2'), ],
                                   },

                        'client' : { 'label'    : u'Client',
                                     'fields'   : [ (DataTypeFieldString, 'client_first'),
                                                    (DataTypeFieldString, 'client_last'),
                                                    (DataTypeFieldAdress, 'client_addr'), ],
                                   },

                        'order'  : { 'label'    : u'Commande',
                                     'fields'   : [ (DataTypeFieldString, 'order_number'),
                                                    (DataTypeFieldRelation, 'order_product'),
                                                    (DataTypeFieldRelation, 'order_client'),
                                                    (DataTypeFieldInteger, 'order_quanti'), ],
                                   },

                        'cost'   : { 'label'    : u'Frais',
                                     'fields'   : [ (DataTypeFieldString, 'cost_title'),
                                                    (DataTypeFieldFloat, 'cost_price'), ],
                                   },
                     },
          
          AddDataOperation : { 'appro' : { 'label'    : u'Approvisionnement',
                                           'datatype' : (DataType, 'product'),
                                           'displayedfields' : [ (DataTypeFieldString, 'product_name'),
                                                                 (DataTypeFieldFloat, 'product_pri'),
                                                                 (DataTypeFieldInteger, 'product_quan') ],
                                           'fixedfields'     : [ (DataTypeFieldFloat, 'product_co2'), ]
                                          },

                               'newcli' : { 'label'    : u'Nouveau client',
                                            'datatype' : (DataType, 'client'),
                                            'displayedfields' : [ (DataTypeFieldString, 'client_first'),
                                                                  (DataTypeFieldString, 'client_last'),
                                                                  (DataTypeFieldAdress, 'client_addr'), ],
                                          },

                               'neword' : { 'label'    : u'Nouvelle commande',
                                            'datatype' : (DataType, 'order'),
                                            'displayedfields' : [ (DataTypeFieldString, 'order_number'),
                                                                  (DataTypeFieldRelation, 'order_product'),
                                                                  (DataTypeFieldRelation, 'order_client'),
                                                                  (DataTypeFieldInteger, 'order_quanti'), ],
                                          },

                               'newcos' : { 'label'    : u'Saisir note de frais',
                                            'datatype' : (DataType, 'cost'),
                                            'displayedfields' : [ (DataTypeFieldString, 'cost_title'),
                                                                  (DataTypeFieldFloat, 'cost_price'), ],
                                          },

                               'newbuy' : { 'label'    : u'Achat de matériel',
                                            'datatype' : (DataType, 'cost'),
                                            'displayedfields' : [ (DataTypeFieldString, 'cost_title'),
                                                                  (DataTypeFieldFloat, 'cost_price'), ],
                                          },

                             },

          DelDataOperation : { 'delord' : { 'label'    : u'Annuler commande',
                                            'datatype' : (DataType, 'order'),
                                          },
                             },

          UpdateDataOperation : { 'majpro' : { 'label'    : u'Mettre à jour un produit',
                                               'datatype' : (DataType, 'product'),
                                               'updatefields' : [ (DataTypeFieldString, 'product_name'),
                                                                  (DataTypeFieldFloat, 'product_pri'),
                                                                  (DataTypeFieldInteger, 'product_quan') ],
                                             },
                                 
                                  'majcli' : { 'label'    : u'Modifier une fiche client',
                                               'datatype' : (DataType, 'client'),
                                               'updatefields' : [ (DataTypeFieldString, 'client_first'),
                                                                  (DataTypeFieldString, 'client_last'),
                                                                  (DataTypeFieldAdress, 'client_addr'), ],
                                             },

                                },

          Perspective : { 'products' : { 'label'    : u'Liste des produits',
                                         'datatype' : (DataType, 'product'),
                                         'datafields' : [ (DataTypeFieldString, 'product_name'),
                                                          (DataTypeFieldFloat, 'product_pri'),
                                                          (DataTypeFieldInteger, 'product_quan'), ],
                                         'operations' : [ (AddDataOperation, 'appro'),
                                                          (UpdateDataOperation, 'majpro'), ]
                                       },
        
                          'clients'  : { 'label'    : u'Liste des clients',
                                         'datatype' : (DataType, 'client'),
                                         'datafields' : [ (DataTypeFieldString, 'client_first'),
                                                          (DataTypeFieldString, 'client_last'),
                                                          (DataTypeFieldAdress, 'client_addr'), ],
                                         'operations' : [ (AddDataOperation, 'newcli'),
                                                          (UpdateDataOperation, 'majcli'), ]
                                       },
        
                          'orders'   : { 'label'    : u'Liste des commandes',
                                         'datatype' : (DataType, 'order'),
                                         'datafields' : [ (DataTypeFieldString, 'order_number'),
                                                          (DataTypeFieldRelation, 'order_product'),
                                                          (DataTypeFieldRelation, 'order_client'),
                                                          (DataTypeFieldInteger, 'order_quanti'), ],
                                         'operations' : [ (AddDataOperation, 'neword'),
                                                          (DelDataOperation, 'delord'), ]
                                       },
        
                          'costs'    : { 'label'    : u'Chiffre d\'affaires',
                                         'datatype' : (DataType, 'cost'),
                                         'datafields' : [ (DataTypeFieldString, 'cost_title'),
                                                          (DataTypeFieldFloat, 'cost_price'), ],
                                         'operations' : []
                                       },
        
                          'stats'    : { 'label'    : u'Statistiques',
                                         'datatype' : (DataType, 'cost'),
                                         'datafields' : [ (DataTypeFieldString, 'cost_title'),
                                                          (DataTypeFieldFloat, 'cost_price'), ],
                                         'operations' : []
                                       },
        
                          'buy'      : { 'label'    : u'Matériel et notes de frais',
                                         'datatype' : (DataType, 'cost'),
                                         'datafields' : [ (DataTypeFieldString, 'cost_title'),
                                                          (DataTypeFieldFloat, 'cost_price'), ],
                                         'operations' : [ (AddDataOperation, 'newcos'),
                                                          (AddDataOperation, 'newbuy'), ]
                                       },
                          },
          }
