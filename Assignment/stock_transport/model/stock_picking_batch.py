# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api
from odoo.exceptions import ValidationError
from odoo.exceptions import UserError

class StockPickingBatch(models.Model):
    _inherit = 'stock.picking.batch'
    
    dock_id = fields.Many2one('stock.transport.dock', 'Dock')
    vehicle_id = fields.Many2one('fleet.vehicle',string="Vehicle")
    vehicle_category_id = fields.Many2one('fleet.vehicle.model.category',string="Vehicle Category")
    weight = fields.Integer(string="Weight",compute="_compute_weight",store=True)
    volume = fields.Integer(string="Volume",compute="_compute_volume",store=True)
    volume_percentage = fields.Integer(string='Volume Percentage', compute='_compute_percentage', store=True)
    weight_percentage = fields.Integer(string='Weight Percentage', compute='_compute_percentage', store=True)
    transfer = fields.Integer(string="Transfer",compute='_compute_transfers', store=True)
    lines = fields.Integer(string="Lines",compute='_compute_lines', store=True)

    @api.depends('volume', 'weight', 'vehicle_category_id.max_volume', 'vehicle_category_id.max_weight')
    def _compute_percentage(self):
        for load in self:
            if load.vehicle_category_id.max_volume and load.volume:
                load.volume_percentage = (load.volume / load.vehicle_category_id.max_volume) * 100
            else:
                load.volume_percentage = 0

            if load.vehicle_category_id.max_weight and load.weight:
                load.weight_percentage = (load.weight / load.vehicle_category_id.max_weight) * 100
            else:
                load.weight_percentage = 0
    
    @api.depends('vehicle_category_id','picking_ids.total_volume_out')
    def _compute_weight(self):
        for rec in self:
            totaL_weight=0
            if(rec.vehicle_category_id):
                for product in rec.picking_ids:
                    totaL_weight+=(product.shipping_weight)
                rec.weight = totaL_weight
            else:
                rec.weight=totaL_weight
            
    @api.depends('vehicle_category_id','picking_ids.total_volume_out')
    def _compute_volume(self):
        for rec in self:
            total_volume=0
            if(rec.vehicle_category_id):
                for product in rec.picking_ids:
                    total_volume+=(product.total_volume_out)
                rec.volume = total_volume
            else:
                rec.volume=total_volume
    
    @api.depends('picking_ids')
    def _compute_transfers(self):
        for rec in self:
            no_transfers=0
            for record in rec.picking_ids:
                no_transfers+=1
            rec.transfer=no_transfers
            
    @api.depends('move_ids')
    def _compute_lines(self):
        for rec in self:
            no_lines=0
            for record in rec.move_ids:
                no_lines+=1
            rec.lines=no_lines
            
    @api.depends('weight','volume','name','vehicle_id')
    def _compute_display_name(self):
        for record in self:
            if(record.vehicle_id):
                record.display_name = (f"{record.name}: {record.volume}kg, {record.weight}m³ {record.vehicle_id.driver_id.name}")    
            else:
                record.display_name = (f"{record.name}: {record.volume}kg, {record.weight}m³")

    @api.constrains('volume')
    def _check_price(self):
        for rec in self:
            if (rec.volume>rec.vehicle_category_id.max_volume):
                raise ValidationError("You can not allow to overload")