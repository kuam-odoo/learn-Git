# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name' : 'Stock inventory',
    'version' : "1.0",
    'depends': ['stock'],
    'license': "LGPL-3",
    'data': [
        'views/res_config_settings_views.xml',
    ],
    'application':True,
    'installable': True,
}