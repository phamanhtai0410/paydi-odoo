
{
    'name': 'Quản lý CRM',
    'category': 'Productivity',
    'description': "Manage Connect to CRMs",
    'summary': 'Manage Connect to CRMs',
    'depends': ['base', 'mail', 'account'],
    'data': [
        'views/res_company_views.xml',
        'security/ir.model.access.csv'
    ],
    'application': True
}
