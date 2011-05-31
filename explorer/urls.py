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
# file: urls.py

from django.conf.urls.defaults import *


urlpatterns = patterns('LegoERP.explorer.views',
    (r'^operation/(?P<viewid>\w+)/(?P<id>\w+)/$','operation'),
    (r'^perspective/(?P<id>\w+)/$','perspective'),
    (r'^datatype/(?P<viewid>\w+)/(?P<id>\w+)/$','datatype'),
    (r'^datatype/(?P<viewid>\w+)/(?P<id>\w+)/(?P<operationid>\w+)/$','datatype'),
    (r'^$','index'), 
)
