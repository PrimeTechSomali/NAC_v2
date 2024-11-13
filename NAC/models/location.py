from odoo import models, fields, api
from math import radians, sin, cos, sqrt, atan2

class Location(models.Model):
    _name = 'location.management'
    _description = 'Location Management'
    _inherit = ['mail.thread', 'mail.activity.mixin']  # Add this line for chatter

    name = fields.Char(string='Location Name', required=True, track_visibility='onchange')
    latitude = fields.Float(string='Latitude', track_visibility='onchange')
    longitude = fields.Float(string='Longitude', track_visibility='onchange')
    description = fields.Text(string='Description', track_visibility='onchange')

    def distance_to(self, other_location):
        """Calculate distance to another location using Haversine formula."""
        if not other_location or not self.latitude or not self.longitude or not other_location.latitude or not other_location.longitude:
            return 0.0

        # Radius of the Earth in kilometers
        R = 6371.0
        lat1 = radians(self.latitude)
        lon1 = radians(self.longitude)
        lat2 = radians(other_location.latitude)
        lon2 = radians(other_location.longitude)

        dlat = lat2 - lat1
        dlon = lon2 - lon1

        a = sin(dlat / 2)**2 + cos(lat1) * cos(lat2) * sin(dlon / 2)**2
        c = 2 * atan2(sqrt(a), sqrt(1 - a))

        distance = R * c  # in kilometers
        return distance