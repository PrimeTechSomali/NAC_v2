from odoo import models, fields

class Ambulance(models.Model):
    _name = 'ambulance.management'
    _description = 'Ambulance Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line for chatter

    name = fields.Char(string='Ambulance Number', required=True, track_visibility='onchange' )
    model = fields.Char(string='Model', required=True)
    registration_number = fields.Char(string='Registration Number', required=True, track_visibility='onchange')
    status = fields.Selection([
        ('available', 'Available'),
        ('in_service', 'In Service'),
        ('maintenance', 'Under Maintenance'),
        ('out_of_service', 'Out of Service')
    ], string='Status', default='available' , track_visibility='onchange')
    capacity = fields.Integer(string='Capacity', help='Number of patients the ambulance can accommodate' , track_visibility='onchange')
    location = fields.Char(string='Current Location' , track_visibility='onchange')
    last_service_date = fields.Date(string='Last Service Date', track_visibility='onchange')
    next_service_due = fields.Date(string='Next Service Due Date', track_visibility='onchange')
    fuel_level = fields.Float(string='Fuel Level (%)', default=100.0, track_visibility='onchange')
    driver_id = fields.Many2one('staff.management', string='Assigned Driver', track_visibility='onchange')
    emergency_equipment_ids = fields.Many2many('equipment.management', string='Emergency Equipment', track_visibility='onchange')
    is_available = fields.Boolean(string='Is Available', default=True, track_visibility='onchange')
    current_location = fields.Many2one('location.management', string='Current Location', track_visibility='onchange')
    
    # Related ambulance requests
    related_ambulance_requests = fields.One2many(
        'ambulance.request', 
        'assigned_ambulance_id', 
        string='Related Requests'
    )
