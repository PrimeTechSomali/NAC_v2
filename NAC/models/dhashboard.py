from odoo import models, fields, api

class AmbulanceDashboard(models.Model):
    _name = 'ambulance.dashboard'
    _description = 'Ambulance Dashboard'

    available_ambulances_count = fields.Integer(string='Available Ambulances', compute='_compute_dashboard_counts', store=False)
    total_patients_count = fields.Integer(string='Total Patients', compute='_compute_dashboard_counts', store=False)
    total_requests_count = fields.Integer(string='Total Requests', compute='_compute_dashboard_counts', store=False)
    total_in_progress_count = fields.Integer(string='Total Requests In Progress', compute='_compute_dashboard_counts', store=False)
    total_completed_count = fields.Integer(string='Total Completed Requests', compute='_compute_dashboard_counts', store=False)
    total_staff_count = fields.Integer(string='Total Staff', compute='_compute_dashboard_counts', store=False)

    @api.depends('available_ambulances_count', 'total_patients_count', 'total_requests_count', 
                 'total_in_progress_count', 'total_completed_count', 'total_staff_count')
    def _compute_dashboard_counts(self):
        """Compute counts for the dashboard."""
        ambulance_model = self.env['ambulance.management']
        patient_model = self.env['patient.management']
        request_model = self.env['ambulance.request']
        staff_model = self.env['staff.management']

        available_ambulances = ambulance_model.search_count([('status', '=', 'available')])
        total_patients = patient_model.search_count([])
        total_requests = request_model.search_count([])
        total_in_progress = request_model.search_count([('status', '=', 'in_progress')])
        total_completed = request_model.search_count([('status', '=', 'completed')])
        total_staff = staff_model.search_count([])

        for record in self:
            record.available_ambulances_count = available_ambulances
            record.total_patients_count = total_patients
            record.total_requests_count = total_requests
            record.total_in_progress_count = total_in_progress
            record.total_completed_count = total_completed
            record.total_staff_count = total_staff
