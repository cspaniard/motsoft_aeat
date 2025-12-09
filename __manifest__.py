# -*- coding: utf-8 -*-
{
    'name': "motsoft_aeat",

    'summary': "Añade funcionalidades a los módulos OCA de la AEAT.",

    'description': """
Se añaden funcionalidades a los módulos:
    * l10n_es_aeat
    * l10n_es_aeat_mod111
    * l10n_es_aeat_mod115
    * l10n_es_aeat_mod303
    """,

    'author': "David Sanromá",
    'website': "",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/15.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Accounting',
    'version': '17.0.0.1',

    # any module necessary for this one to work correctly
    'depends': [
        'base',
        'l10n_es_aeat',
        'l10n_es_aeat_mod111',
        'l10n_es_aeat_mod115',
        'l10n_es_aeat_mod303',
    ],

    # always loaded
    'data': [
        # 'security/ir.model.access.csv',
        'views/l10n_es_aeat.xml',
        'reports/l10n_es_aeat.xml',
    ],
    # only loaded in demonstration mode
    'demo': [
    ],
}
