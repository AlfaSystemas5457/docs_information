# -*- coding: utf-8 -*-
{
    'name': "Documentos",
    'summary': "Dar acceso simple y rapido a la información de los empleados y vehiculos",
    'description': """Dar acceso simple y rapido a la información de los empleados y vehiculos""",
    'author': "DGV",
    'website': "https://github.com/AlfaSystemas5457/docs_information",
    'category': 'Uncategorized',
    'version': '0.1',
    'license': 'LGPL-3',

    'depends': ['hr', 'mail', 'fleet'],

    'data': [
        'security/ir.model.access.csv',
        'views/button_information_view.xml',
        'views/docs_information_views.xml',
        'views/button_vehicle_information.xml',
        'views/docs_vehicle_information_view.xml',
        'views/menu.xml',
    ],
}
