# -*- coding: utf-8 -*-
{
    'name': "Beanus VietQR - VN Bank",

    'summary': """
        This is the custom module for Beanus biz.
        """,

    'description': """
        This is the custom module for Beanus biz, including:
            - VN address pre-defined (csv file)
            - Show customer phone and delivery address on sale order
            - 
        
        The master data (.csv file) note:
            - for the 'id' column always use alias ID, the system will automatically assign the real ID.
            - For the relation field, always use the alias ID
    """,

    'author': "Beanus",
    'license':"LGPL-3",
    'website': "http://www.beanbakery.vn",

    # Categories can be used to filter modules in modules listing
    # Check https://github.com/odoo/odoo/blob/14.0/odoo/addons/base/data/ir_module_category_data.xml
    # for the full list
    'category': 'Appication',
    'version': '0.1',
    "application": True,
    "installable": True,

    # any module necessary for this one to work correctly
    'depends': ['base'],

    "images": ["static/description/icon.png"],

    # always loaded
    'data': [
        'data/res.bank.csv',
        # 'data/bank_master_data.xml',
        'views/bank/bank.xml',
        'views/bank/res_bank_account.xml',
        'views/assets.xml'
       
        
    ],
    'qweb': [
        'static/src/js/qr_widget/qrwidget.xml'
    ],
    # web.assets_common: Loaded everywhere (frontend, backend, point of sale).
    # web.assets_backend: Only loaded into the "backend" of the application. By backend, I mean where you login as a user as /web/login. This bundle is excluded from the frontend website.
    # web.assets_frontend: The opposite of web.assets_backend, only loaded into the frontend website.
    # web.assets_qweb: Loads QWeb XML files.
    # web.assets_wysiwyg: Loads assets into the backend wysiwyg text editor.
    # website.assets_editor: Loads assets into the frontend website edit mode.
    # web.assets_tests: Loads assets for frontend testing and tours.
    # web._assets_primary_variables: Used to load custom scss variables for styles.  
    # 'assets': {
    #     'web.report_assets_common':[
    #         "beanbakery_vietqr/reports/report.scss"
    #     ],
    #     'web.assets_backend': [
    #         "beanbakery_vietqr/static/src/js/widget/**/*",
    #     ],
    #     'point_of_sale.assets': [
    #         "beanbakery_vietqr/static/src/js/pos/**/*",
    #         "beanbakery_vietqr/static/src/scss/pos.scss",
    #     ],
    #     'web.assets_qweb': [
    #         'beanbakery_vietqr/static/src/xml/**/*',
    #     ],
    # },
    # only loaded in demonstration mode
    'demo': [
         #'data/master_data.xml'
    ],
    
}
