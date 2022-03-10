from odoo import models, fields

class SaleOrderLine(models.Model):
    _inherit = 'sale.order.line'


    client_order_ref = fields.Char(related="order_id.client_order_ref")
