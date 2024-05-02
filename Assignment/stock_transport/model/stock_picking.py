# -*- coding: utf-8 -*-
# Part of Odoo. See LICENSE file for full copyright and licensing details.

from odoo import fields, models, api


class StockPicking(models.Model):
    _inherit = 'stock.picking'

    total_volume_out = fields.Integer(string="Volume",compute="_compute_volume_out",store=True)
    
    @api.depends('move_ids_without_package','move_ids_without_package.quantity','move_ids_without_package.product_id.volume','move_ids_without_package.product_id.weight')
    def _compute_volume_out(self):
        for rec in self:
            if(rec.move_ids_without_package):
                volume=0
                for product in rec.move_ids_without_package:
                    volume+=(product.product_id.volume*product.quantity)
                rec.total_volume_out=volume
            else:
                rec.total_volume_out=0
        return True
