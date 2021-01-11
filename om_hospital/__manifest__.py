{
    'name': "Hospital Management",
    'version': '12.0.1.0.0',
    'category': 'Extra Tools',
    'summary': 'Module fo managing the Hospitals',
    'sequence': '10',
    'license': 'AGPL-3',
    'author': "Smart Technologies (BD) Ltd",
    'maintainer': 'Odoo Mates',
    'website': 'odoomates.com',
    'depends': ['sale','report_xlsx','board','project_timeline'],
    'demo': [],
    'description': """
    Description text
    """,
    # data files always loaded at installation
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'data/sequence.xml',
        'data/appointment_sequence.xml',
        'data/data.xml',
        'data/cron.xml',
        'data/mail_template.xml',
        'wizards/create_appointment.xml',
        'views/patient.xml',
        'views/appointment.xml',
        'views/doctor.xml',
        'views/lab.xml',
        'views/template.xml',
        'views/settings.xml',
        'views/sale_order.xml',
        'views/dashboard.xml',
        'views/server_action.xml',
        'views/website_form.xml',
        'reports/patient_card.xml',
        'reports/sale_report_inherit.xml',
        'reports/report.xml',
        'reports/appointment.xml',

    ],
    # data files containing optionally loaded demonstration data
    'demo': [

    ],
    'installable': True,
    'application': True,
    'auto install': False,
}

