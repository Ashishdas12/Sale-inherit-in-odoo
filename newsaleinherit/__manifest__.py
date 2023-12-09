# __manifest__.py

{
    'name': 'newsale inherit',
    'version': '1.0',
    'summary': 'Customizations to the Purchase module',
    'author': 'Your Name',
    'depends': ['sale'],
    'data': [
        'security/ir.model.access.csv',
        'views/views.xml',


        # Add paths to your XML files here if you have any views or data to import
    ],
    'installable': True,
    'application': True,
    'auto_install': False,
}