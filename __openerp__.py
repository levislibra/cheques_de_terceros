# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

{
    'name': 'Cheques de terceros',
    'version': '1.0',
    'author': 'Libra Levis',
    'category': 'Financiera',
    'summary': 'Cheques de terceros',
    'description': """
Cheques
===========================

Manejo de cartera de cheques de terceros.

""",
    'website': 'www.levislibra.com.ar',
    'depends': [],
    'test': [
        
    ],

    'data': [
        'cheques_de_terceros_view.xml',
        'liquidacion_view.xml',

    ],
#    'update_xml': [
#        'cheques_de_terceros_view.xml',
#    ],
    'installable': True,
    'auto_install': False,
}