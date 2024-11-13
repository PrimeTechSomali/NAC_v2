from odoo import models, fields

class ServiceLog(models.Model):
    _name = 'service.log'
    _description = 'Service Log'

    ambulance_id = fields.Many2one('ambulance.management', string='Ambulance', required=True)
    service_date = fields.Date(string='Service Date', required=True)
    service_type = fields.Selection([
        ('maintenance', 'Maintenance'),
        ('inspection', 'Inspection'),
        ('repair', 'Repair')
    ], string='Service Type', required=True)
    notes = fields.Text(string='Notes')
