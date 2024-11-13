# __manifest__.py

{
    'name': 'National Ambulance Management System',
    'version': '1.0',
    'category': 'Healthcare',
    'summary': 'Manage Ambulance Services for the Ministry of Health Somalia',
    'description': """
        A comprehensive ambulance management system for tracking ambulance requests,
        managing ambulances, staff, equipment, and patient information.
    """,
    'author': 'PrimeTech',
    'depends': ['base', 'mail'],
    'data': [
        'security/ir.model.access.csv',
        'security/security.xml',
        'views/ambulance_views.xml',
        'views/ambulance_request_views.xml',
        'views/equipment_views.xml',
        'views/patient_views.xml',
        'views/service_log_views.xml',
        'views/staff_views.xml',
        'views/location_views.xml',
        'views/dhashboard_view.xml',
        'data/ambulance_request_sequence.xml',
    ],
    'installable': True,
    'application': True,
    'icon': '/NAC/static/description/icon.png',
}
