{
    'name': 'Account POS Machines',
    'version': '0.1',
    'summary': 'Summery',
    'description': 'Description',
    'category': 'Sales',
    'depends': ['mail', 'master_data', 'stock'],
    'data': [
        # 'views/account_pos_machines_view.xml',
        'views/stock_move_line.xml',
        'security/ir.model.access.csv',
        # 'views/wizard.pos.setting.xml',
        # 'views/pos.machine.setting.view.xml',
        'views/res_partner_views.xml',

    ],
    'demo': [],
    'installable': True,
    'auto_install': False,
    'application': True
}
