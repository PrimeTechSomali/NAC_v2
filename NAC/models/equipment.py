from odoo import models, fields

class Equipment(models.Model):
    _name = 'equipment.management'
    _description = 'Equipment Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line for chatter

    name = fields.Char(string='Equipment Name', required=True, track_visibility='onchange')
    quantity = fields.Integer(string='Quantity', default=1, track_visibility='onchange')
    status = fields.Selection([
        ('available', 'Available'),
        ('in_use', 'In Use'),
        ('needs_replacement', 'Needs Replacement')
    ], string='Status', default='available', track_visibility='onchange')
