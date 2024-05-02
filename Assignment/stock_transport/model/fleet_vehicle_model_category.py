# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class FleetVehicleModelCategory(models.Model):
    _inherit = 'fleet.vehicle.model.category'

    max_weight = fields.Integer(string="Max Weight (kg)")
    max_volume = fields.Integer(string="Max Volume (m³)")
    
    @api.depends('max_weight','max_volume','name')
    def _compute_display_name(self):
        for record in self:
            record.display_name = (f"{record.name} ({record.max_weight}kg, {record.max_volume}m³)")
