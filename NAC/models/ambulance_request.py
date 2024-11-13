from odoo import models, fields, api
from odoo.exceptions import UserError
from datetime import datetime, timedelta
import random
import logging

_logger = logging.getLogger(__name__)

class AmbulanceRequest(models.Model):
    _name = 'ambulance.request'
    _description = 'Codsiga Ambulance'
    _inherit = ['mail.thread', 'mail.activity.mixin']

    name = fields.Char(
        string='Request ID', required=True, readonly=True,
        default=lambda self: self.env['ir.sequence'].next_by_code('ambulance.request'),
        track_visibility='onchange'
    )
    patient_id = fields.Many2one('patient.management', string='Bukaan', required=True, track_visibility='onchange')
    pickup_location = fields.Many2one('location.management', string='Goob Qaadista', required=True, track_visibility='onchange')
    destination_location = fields.Many2one('location.management', string='Goobta Loo Wado', required=True, track_visibility='onchange')
    patient_condition = fields.Text(string='Sharaxaadda Xaaladda', track_visibility='onchange')
    request_time = fields.Datetime(string='Waqtiga Codsiga', default=fields.Datetime.now)
    scheduled_time = fields.Datetime(string='Scheduled Time')
    completed_time = fields.Datetime(string='Waqtiga Dhameysashada')
    caller_name = fields.Char(string='Caller Name', track_visibility='onchange')
    caller_phone = fields.Char(string='Caller Phone', track_visibility='onchange')
    assigned_ambulance_id = fields.Many2one('ambulance.management', string='Ambulance-ka La Xiriray', track_visibility='onchange')
    status = fields.Selection([
        ('pending', 'Sugitaan'),
        ('in_progress', 'Dhex-socda'),
        ('completed', 'Dhameysay'),
        ('canceled', 'Laga Tirtiray')
    ], string='Xaaladda', default='pending', tracking=True)
    driver_id = fields.Many2one('staff.management', string='Darawalka La Xiriray', track_visibility='onchange')
    response_time = fields.Float(string='Waqtiga Jawaabta (daqiiqado)', compute='_compute_response_time', store=True)
    
    priority = fields.Selection([
        ('low', 'Hoose'),
        ('medium', 'Dhexdhexaad'),
        ('high', 'Sare'),
        ('critical', 'Qatar')
    ], string='Mudnaanta', required=True, track_visibility='onchange')
    
    incident_priority = fields.Selection([
        ('immediate', 'Immediate'),
        ('queued', 'Queued'),
        ('schedule', 'Schedule'),
    ], string='Incident Priority', store=True)
    
    eta = fields.Datetime(string='Waqtiga La Gaadhi Karo', compute='_compute_eta', store=True)
    
    incident_state = fields.Selection([
        ('reported', 'Emergency Reported'),
        ('dispatched', 'Response Dispatched'),
        ('on_scene', 'Arrive On-Scene'),
        ('intervention', 'On-Scene Intervention & Transport'),
        ('reporting', 'Reporting')
    ], string='Incident State', default='reported', track_visibility='onchange')

    @api.depends('request_time', 'completed_time')
    def _compute_response_time(self):
        for record in self:
            if record.status == 'completed' and record.completed_time:
                response_duration = (record.completed_time - record.request_time).total_seconds() / 60.0
                record.response_time = response_duration

    @api.depends('pickup_location', 'assigned_ambulance_id')
    def _compute_eta(self):
        for record in self:
            if record.pickup_location and record.assigned_ambulance_id and record.assigned_ambulance_id.current_location:
                distance = record.pickup_location.distance_to(record.assigned_ambulance_id.current_location)
                average_speed_kmh = 60 * (1 + random.uniform(-0.2, 0.2))
                record.eta = fields.Datetime.add(record.request_time, timedelta(hours=distance / average_speed_kmh))
            else:
                record.eta = False

    @api.model
    def assign_scheduled_ambulances(self):
        """Assign scheduled ambulances automatically at the specified scheduled time."""
        current_time = fields.Datetime.now()
        requests = self.search([('incident_priority', '=', 'schedule'), ('scheduled_time', '<=', current_time), ('status', '=', 'pending')])
        for request in requests:
            request.intelligent_assign_ambulance()

    def intelligent_assign_ambulance(self):
        """Automatically assign the nearest available ambulance to pending requests."""
        for request in self:
            if request.status == 'pending':
                available_ambulances = self.env['ambulance.management'].search([('status', '=', 'available')])
                nearest_ambulance = min(
                    available_ambulances,
                    key=lambda amb: amb.current_location.distance_to(request.pickup_location),
                    default=None
                )
                
                if nearest_ambulance:
                    request.assigned_ambulance_id = nearest_ambulance.id
                    request.status = 'in_progress'
                    nearest_ambulance.status = 'in_service'
                    nearest_ambulance.is_available = False
                    _logger.info(f"Assigned ambulance {nearest_ambulance.name} to request {request.name}.")
                    request.message_post(body=f"Assigned ambulance {nearest_ambulance.name} to the request.")
                else:
                    _logger.warning("All ambulances are busy. Cannot assign.")
                    raise UserError("Dhamaan Ambulance-yadu waa wada buuxan. Fadlan sug.")

    def broadcast_incident(self):
        """Broadcasts the incident to all ambulances without changing their status."""
        ambulances = self.env['ambulance.management'].search([])  # Fetch all ambulances
        for ambulance in ambulances:
            # Subscribe the ambulance's partner to track messages and post a broadcast message
            self.message_subscribe(partner_ids=[ambulance.partner_id.id])
            ambulance.message_post(body=f"Incident {self.name} broadcasted to this ambulance.")
        self.message_post(body="Incident broadcasted to all ambulances.")
        _logger.info(f"Incident {self.name} broadcasted to all ambulances.")


    def action_set_pending(self):
        for record in self:
            record.status = 'pending'
            record.message_post(body="Status changed to 'pending'.")

    def action_set_in_progress(self):
        for record in self:
            record.status = 'in_progress'
            record.message_post(body="Status changed to 'in progress'.")

    def action_set_completed(self):
        for record in self:
            record.status = 'completed'
            record.completed_time = fields.Datetime.now()
            record.message_post(body="Request marked as completed.")
            
            if record.assigned_ambulance_id:
                record.assigned_ambulance_id.status = 'available'
                record.assigned_ambulance_id.is_available = True
                if record.driver_id:
                    record.driver_id.is_available = True
                _logger.info(f"Request {record.name} completed. Ambulance {record.assigned_ambulance_id.name} is now available.")

            in_progress_requests = self.env['ambulance.request'].search([
                ('status', '=', 'pending'),
                ('assigned_ambulance_id', '=', False)
            ])
            
            if in_progress_requests:
                for request in in_progress_requests:
                    _logger.info(f"Found in-progress request {request.name} with no assigned ambulance. Attempting to assign now.")
                    request.intelligent_assign_ambulance()
                _logger.info(f"Checked in-progress requests. Total found: {len(in_progress_requests)}.")
            else:
                _logger.info("No in-progress requests without assigned ambulances found.")

    def action_set_canceled(self):
        for record in self:
            record.status = 'canceled'
            record.message_post(body="Request has been canceled.")

    # Actions for changing incident states
    def action_set_reported(self):
        self.incident_state = 'reported'
        self.message_post(body="Incident state changed to 'reported'.")

    def action_set_dispatched(self):
        self.incident_state = 'dispatched'
        self.message_post(body="Incident state changed to 'dispatched'.")

    def action_set_on_scene(self):
        self.incident_state = 'on_scene'
        self.message_post(body="Incident state changed to 'on_scene'.")

    def action_set_intervention(self):
        self.incident_state = 'intervention'
        self.message_post(body="Incident state changed to 'intervention'.")

    def action_set_reporting(self):
        self.incident_state = 'reporting'
        self.message_post(body="Incident state changed to 'reporting'.")
