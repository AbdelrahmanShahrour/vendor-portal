{
    'name': 'Base Partner to Product Sales Portal',
    'version': '1.0',
    'author': 'Abdalrahman Shahrour',
    'category': 'Website',
    'depends': ['portal', 'contacts', 'sale', 'stock', 'purchase'],
    'data': [
        'views/res_partner_view.xml',
    ],
    'installable': True,
    'application': False,
    'auto_install': False,
}