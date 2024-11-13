from odoo import models, fields

class Staff(models.Model):
    _name = 'staff.management'
    _description = 'Staff Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line for chatter

    name = fields.Char(string='Staff Name', required=True, track_visibility='onchange')
    position = fields.Char(string='Position', required=True, track_visibility='onchange')
    contact_number = fields.Char(string='Contact Number', required=True, track_visibility='onchange')
    email = fields.Char(string='Email', track_visibility='onchange')
    assigned_ambulance_ids = fields.One2many('ambulance.management', 'driver_id', string='Assigned Ambulances', track_visibility='onchange')
    is_available = fields.Boolean(string='Is Available', default=True, track_visibility='onchange')