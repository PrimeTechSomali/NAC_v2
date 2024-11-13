from odoo import models, fields

class Patient(models.Model):
    _name = 'patient.management'
    _description = 'Patient Management for National Ambulance Service'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line for chatter

    name = fields.Char(string='Patient Name', required=True , track_visibility='onchange')
    age = fields.Integer(string='Age', track_visibility='onchange')
    gender = fields.Selection([
        ('male', 'Male'),
        ('female', 'Female'),
        ('other', 'Other')
    ], string='Gender')
    medical_history = fields.Text(string='Medical History', track_visibility='onchange')
    contact_number = fields.Char(string='Contact Number', track_visibility='onchange')
    address = fields.Char(string='Address', track_visibility='onchange')

    # Emergency Contact Information
    emergency_contact_name = fields.Char(string='Emergency Contact Name', track_visibility='onchange')
    emergency_contact_relationship = fields.Char(string='Emergency Contact Relationship', track_visibility='onchange')
    emergency_contact_phone = fields.Char(string='Emergency Contact Phone Number')
    emergency_contact_address = fields.Char(string='Emergency Contact Address')

    # Medical Information
    current_medications = fields.Text(string='Current Medications')
    allergies = fields.Text(string='Allergies')
    chronic_conditions = fields.Text(string='Chronic Conditions')
    past_surgeries = fields.Text(string='Past Surgeries/Procedures')

    # Ambulance Service Specifics
    service_type = fields.Selection([
        ('emergency', 'Emergency'),
        ('non_emergency', 'Non-Emergency')
    ], string='Type of Service')
    transportation_mode = fields.Selection([
        ('wheelchair', 'Wheelchair'),
        ('stretcher', 'Stretcher'),
        ('normal', 'Normal Transport')
    ], string='Mode of Transportation')

    # Current Condition Details
    chief_complaint = fields.Text(string='Chief Complaint')
    onset_of_symptoms = fields.Datetime(string='Onset of Symptoms')
    duration_of_symptoms = fields.Integer(string='Duration of Symptoms (in hours)')
    pain_level = fields.Integer(string='Pain Level (1-10)', help='Rate pain from 1 (minimal) to 10 (severe)')
    associated_symptoms = fields.Text(string='Associated Symptoms')
    recent_travel_history = fields.Text(string='Recent Travel History')

    # Vital Signs
    blood_pressure = fields.Char(string='Blood Pressure')
    heart_rate = fields.Integer(string='Heart Rate')
    respiratory_rate = fields.Integer(string='Respiratory Rate')
    temperature = fields.Float(string='Temperature (°C)')
    oxygen_saturation = fields.Float(string='Oxygen Saturation Level (%)')

    # Accessibility Needs
    mobility_issues = fields.Boolean(string='Mobility Issues')
    language_preference = fields.Char(string='Language Preference')
    cognitive_challenges = fields.Text(string='Cognitive or Communication Challenges')
